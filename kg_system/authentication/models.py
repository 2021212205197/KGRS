from django.db import models

class Node(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    birth = models.IntegerField()
    death = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Relation(models.Model):
    source = models.ForeignKey(Node, related_name='source_relations', on_delete=models.CASCADE)
    target = models.ForeignKey(Node, related_name='target_relations', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    detail = models.TextField()

    def __str__(self):
        return f"{self.source.name} -> {self.target.name}"