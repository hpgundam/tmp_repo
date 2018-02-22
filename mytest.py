#!/usr/bin/env python

class A:
	f1 = 1
	class Meta:
		abstract = True

class B(A):
	f2 = A.f1
	class Meta(A.Meta):
		pass


b = B()
print(b.f1)
print(b.f2)






