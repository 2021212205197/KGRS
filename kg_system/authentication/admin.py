from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Node, Relation

# 注册自定义的 Node 和 Relation 模型
@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'birth', 'death', 'description', 'type')
    search_fields = ('name', 'title', 'type')

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('source', 'target', 'type', 'detail')
    search_fields = ('type', 'detail')
    list_filter = ('type',)