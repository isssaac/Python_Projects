def tri_recursion(k):
  if(k>0):
    result = k+tri_recursion(k-1)
  else:
    result = 0
  return result

print(tri_recursion(6))