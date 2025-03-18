<template>
  <div class="container">
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
import { Network } from 'vis-network/standalone/esm/vis-network'

export default {
  data() {
    return {
      graphData: {
        nodes: [],
        edges: []
      },
      network: null,
      searchKeyword: '',
      selectedNode: null
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
          smooth: true,
          font: {
            size: 14,
            align: 'middle'
          }
        },
        interaction: {
          hover: true
        }
      }
      
      this.network = new Network(
        this.$refs.graphContainer,
        this.graphData,
        options
      )

      // 添加节点点击事件
      this.network.on('click', (params) => {
        if (params.nodes.length) {
          const nodeId = params.nodes[0]
          this.selectedNode = this.graphData.nodes.find(n => n.id === nodeId)
        }
      })
    },

    async loadTangData() {
      try {
        const url = 'http://127.0.0.1:8000/api/kg/graph?dynasty=tang'; // 确认 URL 正确
        console.log('Request URL:', url);
        const response = await this.axios.get(url, { timeout: 5000 }); // 5 秒超时时间
        console.log('API response:', response); // 打印响应数据
        this.processGraphData(response.data);
      } catch (error) {
        console.error('数据加载失败:', error);
      }
    },

    processGraphData(apiData) {
      // 转换节点格式
      const nodes = apiData.nodes.map(node => ({
        id: node.id,
        label: node.name,
        title: node.title,
        birth: node.birth,
        death: node.death,
        description: node.description,
        group: node.type || 'default' // 按类型分组
      }))

      // 转换边格式
      const edges = apiData.links.map(link => ({
        from: link.source,
        to: link.target,
        label: link.type,
        ...(link.detail && { title: link.detail }) // 悬浮显示详情
      }))

      // 更新视图
      this.graphData = {
        nodes,
        edges
      }
      this.network.setData(this.graphData)
    },

    async handleSearch() {
      if (!this.searchKeyword) return
      
      try {
        const response = await this.axios.get('/kg/search', {
          params: {
            q: this.searchKeyword,
            dynasty: 'tang'
          }
        })
        
        console.log('Search response:', response) // 打印搜索响应数据

        if (response.data.ids.length > 0) {
          // 高亮搜索到的节点
          this.network.selectNodes(response.data.ids)
          this.network.focus(response.data.ids[0], {
            scale: 0.8,
            animation: true
          })
        }
      } catch (error) {
        console.error('搜索失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 20px;
}

.search-box {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.node-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  max-width: 400px;
}
</style>