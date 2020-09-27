from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q

from api.serializers import RegisterUserSerializer, LabelSerializer, TodoSerializer
from api.models import Label, Todo

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def LabelView(request, todo_id=None):

    if request.method == "GET" and request.resolver_match.url_name == "todo":

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        try:
            todo = Todo.objects.get(id = todo_id)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found Todo'}, status=404)

        if todo.user != request.user and not todo.assigned_users.filter(username = request.user.username).exists():
            return Response({'error': 'Permission Denied'}, status=403)

        try:
            label = Label.objects.get(todo = todo_id)
        except Label.DoesNotExist:
            return Response({'error': 'Not Found Label'}, status=404)

        label_serializer = LabelSerializer(label, many=False)
        return Response(label_serializer.data, status=200)

    if request.method == "GET" and request.resolver_match.url_name == "labels":
        my_labels = Label.objects.filter(user = request.user)
        return Response(my_labels.values_list('name', flat=True), status=200)

    if request.method == 'PUT' and request.resolver_match.url_name == "todo":

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        todo_check = Todo.objects.filter(Q(id = todo_id) & Q(user = request.user))

        if not todo_check.exists():
            return Response({'error': 'Permission Denied'}, status=403)

        labels = request.data.get('labels', [])
        Label.objects.filter(Q(todo_id = todo_id) & Q(user = request.user)).delete()

        for label_name in labels:
            label = Label()
            label.user = request.user
            label.name = label_name
            label.color = ""
            label.todo_id = todo_id
            label.save()

        return Response({'success': 'Label is created'}, status=201)

    if request.method == 'DELETE' and request.resolver_match.url_name == "labels":

        label_id = request.query_params.get('l', None)

        if not label_id:
            return Response({'error': 'Label id is missing'}, status=400)
        try:
            label = Label.objects.get(id = label_id)
        except Label.DoesNotExist:
            return Response({'error': 'Not Found Label'}, status=404)

        if label.user != request.user:
            return Response({'error': 'Permission Denied'}, status=403)

        label.delete()
        return Response({'success': 'Label is deleted'}, status=200)

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def TodoView(request, todo_id=None):

    if request.method == 'GET' and request.resolver_match.url_name == 'todos':
        todos = Todo.objects.filter(user = request.user).order_by('-updated_at')
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=200)

    if request.method == 'GET' and request.resolver_match.url_name == 'shared_todos':
        todos = Todo.objects.filter(assigned_users = request.user)
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=200)

    if request.method == 'GET' and request.resolver_match.url_name == 'todo':

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        try:
            todo = Todo.objects.get(id = todo_id)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found Todo'}, status=404)

        if todo.user != request.user and not todo.assigned_users.filter(username = request.user.username).exists():
            return Response({'error': 'Permission Denied'}, status=403)

        todo_serializer = TodoSerializer(todo, many=False)

        return Response(todo_serializer.data, status=200)

    if request.method == 'PUT' and request.resolver_match.url_name == 'todos':

        _id = request.data.get('id', None)
        title = request.data.get('title', None)
        status = request.data.get('status', False)
        content = request.data.get('content', '')

        if not title:
            return Response({'error': 'Title is missing'}, status=400)

        if _id: # For Update
            try:
                todo = Todo.objects.get(id = _id)
            except Todo.DoesNotExist:
                return Response({'error': 'Todo not Found'}, status=404)
        
            if todo.user != request.user and not todo.assigned_users.filter(username = request.user.username).exists():
                return Response({'error': 'Permission Denied'}, status=403)
        else:
            todo = Todo()

        if not _id:
            todo.user = request.user

        todo.title = title
        todo.content = content
        todo.status = status
        todo.updated_at = timezone.now()
        if not _id:
            todo.created_at = timezone.now()

        todo.save()
        return Response({'success': 'todo is created', 'id': todo.id}, status=201)

    if request.method == 'POST' and request.resolver_match.url_name == 'users':

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        try:
            todo = Todo.objects.get(id = todo_id)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found Todo'}, status=404)

        if todo.user != request.user:
            return Response({'error': 'Permission Denied'}, status=403)

        errors = []
        success = []
        users = request.data.get('users', [])

        todo.assigned_users.clear()

        for usr in users:
            try:
                user = User.objects.get(username = usr)
            except User.DoesNotExist:
                errors.append({'status': '{} User Not Found'.format(usr)})

            if not todo.assigned_users.filter(username=user.username).exists():
                todo.assigned_users.add(user)
                success.append({'staz'})

        return Response({'success': '', 'errors': errors}, status=200)

    if request.method == 'DELETE' and request.resolver_match.url_name == 'todo':

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        try:
            todo = Todo.objects.get(id = todo_id)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found Todo'}, status=404)

        if todo.user != request.user:
            return Response({'error': 'Permission Denied'}, status=403)

        todo.delete()
        return Response({'success': 'todo is deleted'}, status=200)

    if request.method == 'DELETE' and request.resolver_match.url_name == 'users':

        if not todo_id:
            return Response({'error': 'Todo id is missing'}, status=400)

        try:
            todo = Todo.objects.get(id = todo_id)
        except Todo.DoesNotExist:
            return Response({'error': 'Not Found Todo'}, status=404)

        if todo.user != request.user:
            return Response({'error': 'Permission Denied'}, status=403)

        username = request.query_params.get('u', None)

        if not username:
            return Response({'error': 'Username is missing'}, status=400)

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({'error': 'User not Found'}, status=404)

        if todo.assigned_users.filter(username = username).exists():
            todo.assigned_users.remove(user)
            return Response({'success': 'User removed the todo list'}, status=200)
        
        return Response({'error': 'Bad Request'}, status=400)

@csrf_exempt
@api_view(['POST'])
def UserCreate(request):

    if request.method == "POST":
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'status': True}, status=201)

        return Response(serializer.errors, status=400)
