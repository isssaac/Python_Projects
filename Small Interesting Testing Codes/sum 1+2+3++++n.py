def tri_recursion(x):
  if(x>0):
    result = x+tri_recursion(x-1)
  else:
    result = 0
  return result

print(tri_recursion(6))