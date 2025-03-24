<template>
  <div class="container">
    <!-- 加载提示 -->
    <div v-if="loading" class="loading">数据加载中...</div>
    
    <!-- 可视化容器 -->
    <div ref="graphContainer" class="graph-container"></div>
    
    <!-- 搜索框 -->
    <div class="search-box">
      <input 
        v-model="searchKeyword"
        @keyup.enter="handleSearch"
        placeholder="输入人物名称（如：李白）"
      />
      <button @click="handleSearch">搜索</button>
    </div>
    
    <!-- 节点信息弹窗 -->
    <div v-if="selectedNode" class="node-modal">
      <h3>{{ selectedNode.name }}</h3>
      <p>身份：{{ selectedNode.title }}</p>
      <p v-if="selectedNode.birth">生卒：{{ selectedNode.birth }} - {{ selectedNode.death }}</p>
      <p>{{ selectedNode.description }}</p>
      <button @click="selectedNode = null">关闭</button>
    </div>
  </div>
</template>

<script>
import { Network, DataSet } from 'vis-network/standalone/esm/vis-network'
import axios from 'axios'
import _ from 'lodash'

export default {
  data() {
    return {
      graphData: {
        nodes: new DataSet(),
        edges: new DataSet()
      },
      network: null,
      searchKeyword: '',
      selectedNode: null,
      loading: false
    }
  },
  mounted() {
    this.initNetwork()
    this.loadTangData()
  },
  methods: {
    initNetwork() {
      const options = {
        nodes: {
          shape: 'dot',
          size: 25,
          font: {
            size: 16,
            color: '#333'
          },
          borderWidth: 2,
          shadow: true
        },
        edges: {
          arrows: 'to',
          smooth: {
            type: 'dynamic'
          },
          font: {
            size: 14,
            align: 'middle'
          }
        },
        groups: {
          poet: {
            color: {
              background: '#9CCC65',
              border: '#689F38'
            }
          },
          emperor: {
            color: {
              background: '#FF8A65',
              border: '#E64A19'
            }
          },
          official: {
            color: {
              background: '#64B5F6',
              border: '#1976D2'
            }
          }
        },
        physics: {
          enabled: true,
          barnesHut: {
            gravitationalConstant: -30000,
            centralGravity: 0.3,
            springLength: 200,
            springConstant: 0.04,
            damping: 0.09,
            avoidOverlap: 1
          },
          stabilization: {
            enabled: true,
            iterations: 200,
            updateInterval: 25
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 200,
          hideEdgesOnDrag: true
        }
      }

      this.network = new Network(
        this.$refs.graphContainer,
        this.graphData,
        options
      )

      // 点击任意位置关闭弹窗
      this.network.on('click', (params) => {
        this.selectedNode = params.nodes.length 
          ? this.graphData.nodes.get(params.nodes[0])
          : null
      })
    },

    async loadTangData() {
      this.loading = true
      try {
        const response = await axios.get('http://127.0.0.1:8000/zh-hans/api/kg/graph/', {
          params: { dynasty: 'tang' },
          timeout: 5000
        })
        this.processGraphData(response.data)
      } catch (error) {
        this.showError('数据加载失败')
      } finally {
        this.loading = false
      }
    },

    processGraphData(apiData) {
      if (!apiData?.nodes || !apiData?.edges) {
        this.showError('数据格式错误')
        return
      }

      const nodeMap = new Map()
      const nodes = apiData.nodes.map(node => {
        const nodeConfig = {
          id: node.id,
          label: node.name,
          title: node.title,
          birth: node.birth,
          death: node.death,
          description: node.description,
          group: node.type || 'default'
        }
        nodeMap.set(node.id, nodeConfig)
        return nodeConfig
      })

      const edges = apiData.edges.map(edge => ({
        from: edge.from,
        to: edge.to,
        label: edge.label,
        title: edge.title || `${nodeMap.get(edge.from)?.label} → ${nodeMap.get(edge.to)?.label}`
      }))

      this.graphData.nodes.clear()
      this.graphData.edges.clear()
      this.graphData.nodes.add(nodes)
      this.graphData.edges.add(edges)

      // 自动调整视图
      this.network.fit({
        animation: {
          duration: 1000,
          easingFunction: 'easeInOutQuad'
        }
      })
    },

    handleSearch: _.debounce(function() {
      if (!this.searchKeyword.trim()) return
      
      axios.get('http://127.0.0.1:8000/zh-hans/api/kg/search', {
        params: {
          q: this.searchKeyword,
          dynasty: 'tang'
        }
      }).then(response => {
        if (response.data.ids?.length) {
          const nodeIds = response.data.ids.map(Number)
          this.network.selectNodes(nodeIds)
          this.network.focus(nodeIds[0], {
            scale: 0.8,
            animation: true
          })
        }
      }).catch(() => {
        this.showError('搜索失败，请重试')
      })
    }, 500),

    showError(message) {
      alert(message)
    }
  }
}
</script>

<style scoped>
.container {
  position: relative;
  min-height: 100vh;
  padding: 20px;
  background: #f5f5f5;
}

.graph-container {
  height: calc(100vh - 120px);
  width: calc(100% - 40px);
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.search-box {
  position: absolute;
  top: 40px;
  right: 40px;
  z-index: 100;
  display: flex;
  gap: 10px;
  background: rgba(255, 255, 255, 0.95);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.search-box input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 280px;
}

.search-box button {
  padding: 8px 16px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.search-box button:hover {
  background: #1976D2;
}

.node-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  max-width: 480px;
  z-index: 200;
}

.node-modal h3 {
  color: #2196F3;
  margin-bottom: 12px;
}

.loading {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #2196F3;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .graph-container {
    height: calc(100vh - 160px);
    width: calc(100% - 20px);
  }

  .search-box {
    top: 20px;
    right: 20px;
    left: 20px;
    min-width: auto;
  }

  .search-box input {
    flex: 1;
    min-width: auto;
  }

  .node-modal {
    width: 90vw;
    padding: 16px;
  }
}
</style>
