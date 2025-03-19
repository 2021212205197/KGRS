from django.contrib.auth import authenticate, login as django_login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.shortcuts import render
from .serializers import UserSerializer
from django.http import JsonResponse
import json
from .neo4j_utils import driver, process_neo4j_data, get_tang_graph
import logging

logger = logging.getLogger(__name__)

# 根路径视图
def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def register(request):
    """用户注册视图"""
    username = request.data.get('username')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({"message": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"message": "邮箱已存在"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """用户登录视图"""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        django_login(request, user)
        user_data = {
            "username": user.username,
            "email": user.email
        }
        return Response({"message": "登录成功", "user": user_data}, status=status.HTTP_200_OK)
    return Response({"error": "无效的凭据"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def kg_graph(request):
    """统一知识图谱接口"""
    try:
        # 获取朝代参数
        dynasty_type = request.GET.get('dynasty', '').lower()
        logger.info(f"Received request for dynasty: {dynasty_type}")
        
        # 唐朝知识图谱处理
        if dynasty_type == 'tang':
            graph = get_tang_graph()
            query = """
            MATCH (n:TangDynasty)-[r]->(m)
            RETURN n{.id, .name, .title, .birth, .death, .description} as n,
                   r{.type, .detail} as r,
                   m{.id, .name, .title, .birth, .death, .description} as m
            LIMIT 200
            """
            result = graph.run(query)
            logger.info(f"Tang graph query result: {list(result)}")
            # 调试输出
            print(f"Tang graph query result: {list(result)}")
            return JsonResponse(process_neo4j_data(result))
        
        # 默认知识图谱处理
        with driver.get_session() as session:
            query = """
            MATCH (p:Person)-[r]->(p2)
            RETURN p{.id, .name, .title, .birth, .death, .description} as p,
                   r{.type, .detail} as r,
                   p2{.id, .name, .title, .birth, .death, .description} as p2
            LIMIT 200
            """
            result = session.run(query)
            logger.info(f"Default graph query result: {list(result)}")
            # 调试输出
            print(f"Default graph query result: {list(result)}")
            return JsonResponse(process_neo4j_data(result))

    except Exception as e:
        logger.error(f"Error in kg_graph: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def kg_search(request):
    """统一图谱搜索接口"""
    try:
        query = request.GET.get('q', '')
        dynasty_type = request.GET.get('dynasty', '').lower()
        
        # 唐朝专用搜索
        if dynasty_type == 'tang':
            graph = get_tang_graph()
            result = graph.run(
                "MATCH (n:TangDynasty) WHERE toLower(n.name) CONTAINS toLower($name) "
                "RETURN n.id as id",
                {'name': query}
            )
            ids = [record['id'] for record in result]
            return JsonResponse({'ids': ids})
        
        # 默认搜索
        with driver.get_session() as session:
            result = session.run(
                "MATCH (p:Person) WHERE toLower(p.name) CONTAINS toLower($name) "
                "RETURN p.id as id",
                {'name': query}
            )
            ids = [record['id'] for record in result]
            return JsonResponse({'ids': ids})

    except Exception as e:
        logger.error(f"Error in kg_search: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
