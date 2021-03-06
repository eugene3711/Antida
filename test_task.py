import math

#функция, решающая уравнение
def solve(a,b,c):

  print(f"Ваше уравнение: \n \t {a}x^2+{b}x+{c}=0")

  disk = b*b-4*a*c

  print("Дискриминант: {:.3f}".format(disk))

  if disk < 0:
    print("Нет действительных корней")
  elif disk == 0:
    x = -b/2*a
    print("Единственный корень: х = {:.3f}".format(x))
  else:
    x1 = (-b+math.sqrt(disk))/(2*a)
    x2 = (-b-math.sqrt(disk))/(2*a)
    print("Корни: x1 = {:.3f}, x2 = {:.3f}".format(x1,x2))
    


# функция ввода чисел, проверяет их, переводит ввод из str во float 
# дает право 5 неверных вводов на каждый коэффициент
def getNumber(coef):
  patience = 5
  while (patience > 0):
    number = input(f'Введите "{coef}"\n')
    try:
        number = float(number)
        
    except:
        number = 'error'
    if number == 'error' or (coef=="a" and number == 0):
      print("Введите вещественное число, пожалуйста, a!=0 \n")
      patience -= 1
      continue
    else:
      return number
  if patience == 0:
    print("Возвращайтесь позже с числами!")
    quit()    
  

proceed = True
while (proceed):
  print("Квадратное уравнение имеет вид:\n\t ax^2+bx+c=0")
  
  a = getNumber("a")
  
  b = getNumber("b")
  
  c = getNumber("c")


  solve(a,b,c)
  
  proceed = bool(input("Введите что-нибудь, чтобы посчитать еще \n или оставьте строку пустой, чтобы выйти \n"))
  if proceed == False:
    print("Всего вам доброго, учите математику и Python!")
