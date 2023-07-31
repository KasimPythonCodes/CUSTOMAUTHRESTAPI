from django.shortcuts import render ,HttpResponse
from app.models import UserRegistration
from django.contrib import  messages
from rest_framework import serializers ,status ,response ,generics ,permissions ,views
from app.serializers import UserRegistrationSerializer ,LoginSerializer ,UserProfile
from django.contrib.auth.hashers import make_password ,check_password
from django.contrib.auth.models import User
import jwt
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
# l={
#     'kasim':1
# }
# print(jwt.encode(l,'secret',algorithm='HS256').decode())


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistraionSerializerApi(views.APIView):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer
    # def get(self , request):
    #     udata=UserRegistration.objects.all()
    #     serializer = self.serializer_class(udata ,many=True)
    #     return response.Response(serializer.data , status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data )
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        if UserRegistration.objects.filter(username=username).exists():
            raise serializers.ValidationError("This Username is already exists ")
        elif UserRegistration.objects.filter(email=email).exists():
            raise serializers.ValidationError("This Email is already exists ")
        else:
            user= UserRegistration.objects.create(username=username,first_name=first_name,last_name=last_name ,email=email ,password=make_password(password))
            user.save()
            token = get_tokens_for_user(user)
            return response.Response({'token' : token ,'msg':'Registration Successfully' } , status=status.HTTP_201_CREATED)




class UserLoginApi(generics.GenericAPIView):
    queryset = UserRegistration.objects.all()
    serializer_class=LoginSerializer   
    def post(self , request):  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email =serializer.data.get('email')
        password = serializer.data.get('password')
        
        if UserRegistration.objects.filter(email=email).exists():
            current_user = UserRegistration.objects.get(email=email)
            flag = check_password(password , current_user.password)
            if flag:
                request.session['current_user'] = current_user.id 
                token = get_tokens_for_user(current_user)
                return response.Response({'token':token , 'msg':f'login successfully!! {current_user.id}' })
            else:
                raise serializers.ValidationError("Email or password is Invalid !!")
        else:
            raise serializers.ValidationError("User This  Email Not Registered !!")
        return response.Response(serializer.data , status=status.HTTP_200_OK)



"""
class UserLoginApi(generics.GenericAPIView):
    queryset = UserRegistration.objects.all()
    serializer_class=LoginSerializer   
    def post(self , request):  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email =serializer.data.get('email')
        password = serializer.data.get('password')
        
        if UserRegistration.objects.filter(email=email).exists():
            current_user = UserRegistration.objects.get(email=email)
            flag = check_password(password , current_user.password)
            if flag:
                request.session['current_user'] = current_user.id 
                token = get_tokens_for_user(current_user)
                return response.Response({'token':token , 'msg':f'login successfully!! {current_user.id}' })
            else:
                raise serializers.ValidationError("Email or password is Invalid !!")
        else:
            raise serializers.ValidationError("User This  Email Not Registered !!")
        return response.Response(serializer.data , status=status.HTTP_200_OK)


"""
class UserProfileApi(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self , request):
        try:
            current_user = request.session.get('current_user')
            current_user = UserRegistration.objects.get(id=current_user)
            serializer = UserProfile(current_user)
            return response.Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            raise serializers.ValidationError(e)

    

def UserViews(request):
    current_user = request.session.get('current_user')
    user = UserRegistration.objects.get(id=current_user)
    obj=UserRegistration.objects.all()
    return render(request , 'index.html',{'user':user ,'obj':obj})

def Registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        UserRegistration(username=username,first_name=fname ,last_name=lname , email=email , password=make_password(password)).save()
        messages.success(request , " Registration is successfully!! ")
    return render(request , 'registration.html' )

def Login_User(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if UserRegistration.objects.filter(email=email).exists():
            current_user= UserRegistration.objects.get(email=email)
            flag = check_password(password , current_user.password)
            if flag:    
                request.session['current_user'] = current_user.id
                # User Check Permissions in  DB or Code #######
                return HttpResponse(f"Home Page {current_user.id}")
            else : 
                messages.info(request , "Email or Password invalid !!")
        else:
            messages.info(request , "This Email is not registered !!")
    return render(request ,'login.html')        
            

























# def Index(request):
#     bookname = request.COOKIES['bookname']
#     response = render(request , 'index.html',{'bookname':bookname})
#     response.set_cookie('bookname','1')
#     return response


# def SetCookie(request):
#     response = HttpResponse("set cookies")
#     response.set_cookie('bookname','1')
#     return response
 
# def GetCookie(request):
#     bookname = request.COOKIES['bookname']
#     return HttpResponse(f'The book name is: {bookname}')

# def Plus(request):
#     if request.method == 'GET':
#         r= request.GET.get('prod_id')
#         for i in r:
#             r = int(i) + int(r)
#             f=int(i)+int(r)
#             print(f,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
#         data = {
#             'qt':f,
#         }
#         return JsonResponse(data)



# # def plus_cart(request):
# #    if request.method == 'GET':
# #      prod_id=request.GET['prod_id']
# #      c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
# #      c.quantity+=1
# #      c.save()
# #      amount=0.0
# #      shipping_amount=70.0
# #      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
# #      for p in cart_product:
# #         tempamount=(p.quantity*p.product.descounted_price)
# #         amount += tempamount
        

# #      data={
# #           'quantity':c.quantity,
# #           'amount':amount,
# #           'totalamount':amount+shipping_amount

# #         }
# #      return JsonResponse(data)