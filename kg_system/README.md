KGRS/
├── kg_system/                # Django 后端核心系统（活跃维护中）
│   ├── kg_system/            # Django 主配置目录（来自图片内容）
│   │   ├── __pycache__/      # Python字节码缓存（自动生成）
│   │   ├── __init__.py       # 包初始化文件
│   │   ├── asgi.py          # ASGI服务入口
│   │   ├── settings.py      # 项目配置（2025/3/15 更新）
│   │   ├── urls.py          # 全局路由（2025/3/16 更新）
│   │   └── wsgi.py          # WSGI服务入口
│   ├── authentication/       # 用户认证模块（基于图片内容）  
│   │   ├── migrations/       # 数据库迁移文件（2025/3/11 更新）  
│   │   ├── __init__.py       # 模块初始化  
│   │   ├── admin.py          # Django Admin配置（2025/3/11 更新）  
│   │   ├── apps.py           # 应用配置（定义应用名称）  
│   │   ├── models.py         # 用户模型（2025/3/11 更新）  
│   │   ├── neo4j_utils.py    # Neo4j图数据库操作工具（2025/3/16 更新）  
│   │   ├── serializers.py    # DRF序列化器（2025/3/15 更新）  
│   │   ├── tests.py          # 单元测试  
│   │   ├── urls.py           # 认证路由（2025/3/16 更新）  
│   │   └── views.py          # 认证视图（最新修改）  
│   ├── data/                 # 数据处理模块（新增）
│   ├── static/               # 静态资源（CSS/JS/图片）
│   ├── templates/            # HTML模板（兼容前后端混合模式）
│   ├── manage.py             # Django命令行工具
│   └── requirements.txt      # Python依赖清单（含Django 4.2）
├── my-website/               # Vue.js 前端项目（更新于2025/3/18）
│   ├── src/                  # 前端源码（Vue组件/路由/状态管理）
│   │   ├── assets/           # 静态资源（图片/样式）
│   │   ├── components/       # 可复用Vue组件
│   │   ├── router/           # 路由配置（Vue Router）
│   │   ├── utils/            # 工具函数（最新更新）
│   │   ├── views/            # 页面级组件
│   │   ├── App.vue           # 根组件（入口）
│   │   └── main.js           # 全局配置（Vue实例初始化）
│   ├── public/               # 静态资源（HTML入口/图标）
│   ├── dist/                 # 构建产物（用于生产环境部署）
│   ├── node_modules/         # 前端依赖库（npm安装生成）
│   ├── package.json          # 前端依赖声明（Vue、Babel等）
│   ├── vue.config.js         # Vue 项目配置（代理/构建优化）
│   └── babel.config.js       # Babel 转译配置（兼容性支持）
└── run_services.bat          # 服务启动脚本（3天前更新）
