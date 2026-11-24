# **Singapore GCE A-Level Further Mathematics — Question 6**



PDF question verified

Total: 10 marks



## **1. Verification against the attached PDF**

I checked the original question in your uploaded **2026 Preliminary Examination — H2 Further Mathematics, Paper 1**, specifically page 4 of the examination paper (PDF page 4).

Your pasted question is affected by PDF text-extraction and formatting errors. However, the mathematical content can be confirmed from the original printed page.

The correct question is:

**Question 6**

In an Argand diagram, the point \\(P\\) represents the complex number \\(z\\) satisfying

\\[ \boxed{|z-9+4i|=3|z-1-4i|} \\]

Let the locus of \\(P\\) be the curve \\(C\\).

**(a)** By letting \\(z=x+iy\\) and finding the Cartesian equation of \\(C\\), show that \\(C\\) is a circle, and state the centre and radius of \\(C\\). [3]

**(b)** Find the exact minimum value of

\\[ \arg(z-9+4i). \\]

[2]

A given complex number \\(a\\), with

\\[ 0<\arg(a)<\frac{\pi}{2}, \\]

has the property that there is exactly one complex number \\(w\\) that satisfies

\\[ |w-9+4i|=3|w-1-4i| \\]

and

\\[ \left|\frac{w-a^\*}{w+a^\*}\right|=1. \\]

**(c)** Find all possible value(s) of \\(a\\) with this property, and state the corresponding value(s) of \\(w\\) in each case. [5]

**Important corrections to your pasted version:**

- The modulus signs are essential in both complex-number equations.
- The multiplier in the first equation is \\(3\\), not \\(3^2\\).
- The second equation involves the modulus of the entire fraction.
- The argument restriction is \\(0<\arg(a)<\frac{\pi}{2}\\).

The above transcription agrees with the original printed question on PDF page 4.

## **2. Solution strategy and mathematical plan**

The question tests three connected Further Mathematics concepts:

| Part | Main concept                               | Required approach                                          |
| ---- | ------------------------------------------ | ---------------------------------------------------------- |
| (a)  | Locus of complex numbers                   | Cartesian expansion and completing the square              |
| (b)  | Argument of a complex number               | Geometry of tangents to a circle                           |
| (c)  | Complex-number modulus and circle tangency | Perpendicular bisector and distance from a point to a line |

The key observation is that all three parts concern the same circle.

We should therefore establish its equation and geometry in part (a), reuse that information in part (b), and use it again to solve the tangency condition in part (c).

## **3. Detailed examination-standard solutions**

### **(a) Find the Cartesian equation, centre and radius [3 marks]**

**Step 1: Express the complex number in Cartesian form.**

Let

\\[ z=x+iy,\qquad x,y\in\mathbb R. \\]

Given

\\[ |z-9+4i|=3|z-1-4i|, \\]

substituting \\(z=x+iy\\),

\\[ |(x-9)+i(y+4)| =3|(x-1)+i(y-4)|. \\]

**Step 2: Apply the modulus formula.**

Using

\\[ |a+bi|^2=a^2+b^2, \\]

and squaring both sides,

\\[ (x-9)^2+(y+4)^2 =9[(x-1)^2+(y-4)^2]. \\]

Expanding,

\\[ x^2-18x+81+y^2+8y+16 \\]

\\[ =9(x^2-2x+1+y^2-8y+16). \\]

Simplifying,

\\[ x^2+y^2-18x+8y+97 \\]

\\[ =9x^2+9y^2-18x-72y+153. \\]

Rearranging,

\\[ 8x^2+8y^2-80y+56=0. \\]

Dividing by 8,

\\[ x^2+y^2-10y+7=0. \\]

**Step 3: Complete the square.**

\\[ x^2+(y^2-10y)+7=0 \\]

\\[ x^2+(y-5)^2-25+7=0. \\]

Hence,

Comparing with the standard equation of a circle,

\\[ (x-h)^2+(y-k)^2=r^2, \\]

we obtain:

**Required answers**

- Centre: \\(\boxed{(0,5)}\\), or \\(5i\\).
- Radius: \\(\boxed{3\sqrt2}\\).

### **(b) Find the exact minimum value of&#x20;**\\(\arg(z-9+4i)\\)**&#x20;[2 marks]**

**Step 1: Interpret the complex number geometrically.**

Let \\(A\\) represent the complex number

\\[ 9-4i. \\]

Thus, \\(A=(9,-4)\\).

For any point \\(P\\) on the circle \\(C\\),

\\[ \arg(z-9+4i) \\]

is the angle made by the vector \\(\overrightarrow{AP}\\) with the positive real axis.

We need to find the minimum possible angle of this vector.

**Step 2: Find the angle of the line joining&#x20;**\\(A\\)**&#x20;to the centre&#x20;**\\(O\\)**.**

From part (a), the centre is

\\[ O=(0,5). \\]

The gradient of \\(AO\\) is

\\[ m=\frac{5-(-4)}{0-9} =-1. \\]

Since \\(A\\) is in the fourth quadrant and \\(O\\) is in the second quadrant, the direction of \\(AO\\), measured from the positive real axis, is

\\[ \arg(O-A)=\frac{3\pi}{4}. \\]

**Step 3: Use the tangent geometry.**

[geometry - The angle between the pair of tangents drawn from a point P to the circle and its locus - Mathematics Stack Exchange](https://images.openai.com/static-rsc-4/aqm4JsduBnE8qpNuSpEoTEXcIrW0XeGRsou7_DkpnkEbQpEvnG9gBfSVGFkaO8Ej-EpPtW-SzC99Fn9O_LKa_C9jCBggsxPdsP7r9sm-CU9gICFWk7Aft1aw53l2dWTphmJdSMjnwKRjFNtKLwR2flognfSECzE7uAUrXtrkX0Q?purpose=inline)

[math.stackexchange.com](https://math.stackexchange.com/questions/4040642/the-angle-between-the-pair-of-tangents-drawn-from-a-point-p-to-the-circle-and-it?utm_source=chatgpt.com)

The minimum argument occurs when \\(AP\\) is a tangent to circle \\(C\\).

Let \\(T\\) be the point of tangency.

Since the radius is perpendicular to the tangent,

\\[ OT\perp AT. \\]

In right-angled triangle \\(AOT\\),

\\[ AO=\sqrt{(9-0)^2+(-4-5)^2} \\]

\\[ =\sqrt{81+81}=9\sqrt2. \\]

Also,

\\[ OT=3\sqrt2. \\]

Let the angle between \\(AO\\) and the tangent \\(AT\\) be \\(\alpha\\).

Then

\\[ \sin\alpha=\frac{OT}{AO} \\]

\\[ =\frac{3\sqrt2}{9\sqrt2} =\frac13. \\]

Therefore,

\\[ \alpha=\sin^{-1}\left(\frac13\right). \\]

**Step 4: Determine the minimum argument.**

The smaller angle between \\(AO\\) and the two tangents is subtracted from the direction angle of \\(AO\\).

Hence,

\\[ \boxed{ \min\arg(z-9+4i) =\frac{3\pi}{4} -\sin^{-1}\left(\frac13\right) } \\]

Exact answer

### **(c) Find all possible values of&#x20;**\\(a\\)**&#x20;and the corresponding values of&#x20;**\\(w\\)**&#x20;[5 marks]**

This is the most demanding part of the question.

The key is to recognise that the second modulus equation represents a straight line in the Argand diagram. The condition that exactly one \\(w\\) exists means that this line must be tangent to the circle \\(C\\).

**Step 1: Interpret the second modulus equation.**

We are given

\\[ \left|\frac{w-a^\*}{w+a^\*}\right|=1. \\]

Using the property of modulus,

\\[ \frac{|w-a^\*|}{|w+a^\*|}=1. \\]

Therefore,

\\[ |w-a^\*|=|w+a^\*|. \\]

This means that the point representing \\(w\\) is equidistant from the two points representing \\(a^\*\\) and \\(-a^\*\\).

Hence, the locus of \\(w\\) is the perpendicular bisector of the line segment joining \\(a^\*\\) and \\(-a^\*\\).

**Step 2: Obtain the Cartesian equation of this straight line.**

Let

\\[ a=\rho(\cos\theta+i\sin\theta), \\]

where

\\[ \rho>0,\qquad 0<\theta<\frac{\pi}{2}. \\]

Then

\\[ a^\*=\rho(\cos\theta-i\sin\theta). \\]

Let

\\[ w=u+iv. \\]

From

\\[ |w-a^\*|=|w+a^\*|, \\]

squaring both sides gives

\\[ |w-a^\*|^2=|w+a^\*|^2. \\]

Expanding,

\\[ (w-a^\*)(w^\*-a) =(w+a^\*)(w^\*+a). \\]

Thus,

\\[ ww^\*-wa-a^\*w^\*+aa^\* \\]

\\[ =ww^\*+wa+a^\*w^\*+aa^\*. \\]

Cancelling common terms,

\\[ wa+a^\*w^\*=0. \\]

Therefore,

\\[ \operatorname{Re}(wa)=0. \\]

Substituting \\(w=u+iv\\) and \\(a=\rho(\cos\theta+i\sin\theta)\\),

\\[ \operatorname{Re} \left[ \rho(u+iv)(\cos\theta+i\sin\theta) \right]=0. \\]

Hence,

\\[ \rho(u\cos\theta-v\sin\theta)=0. \\]

Since \\(\rho>0\\),

\\[ \boxed{u\cos\theta-v\sin\theta=0}. \\]

This is a straight line passing through the origin.

**Step 3: Apply the condition that there is exactly one value of&#x20;**\\(w\\)**.**

Recall from part (a) that the locus of \\(w\\) satisfying the first equation is the circle

\\[ u^2+(v-5)^2=18. \\]

For exactly one complex number \\(w\\) to satisfy both equations, the straight line must intersect the circle at exactly one point.

Therefore, the straight line must be a tangent to the circle.

The perpendicular distance from the centre \\(O=(0,5)\\) to the line

\\[ u\cos\theta-v\sin\theta=0 \\]

must equal the radius \\(3\sqrt2\\).

Using the perpendicular-distance formula,

\\[ \frac{|0\cos\theta-5\sin\theta|} {\sqrt{\cos^2\theta+\sin^2\theta}} =3\sqrt2. \\]

Since \\(0<\theta<\frac{\pi}{2}\\),

\\[ 5\sin\theta=3\sqrt2. \\]

Therefore,

\\[ \boxed{\sin\theta=\frac{3\sqrt2}{5}}. \\]

As \\(\theta\\) is in the first quadrant,

\\[ \cos\theta =\sqrt{1-\sin^2\theta} \\]

\\[ =\sqrt{1-\frac{18}{25}} =\frac{\sqrt7}{5}. \\]

Consequently,

\\[ \boxed{ \theta=\sin^{-1}\left(\frac{3\sqrt2}{5}\right) }. \\]

**Step 4: Find all possible values of&#x20;**\\(a\\)**.**

Recall that

\\[ a=\rho(\cos\theta+i\sin\theta). \\]

Substituting the exact values,

\\[ a=\rho\left( \frac{\sqrt7}{5} +i\frac{3\sqrt2}{5} \right). \\]

Hence, all possible values of \\(a\\) are

\\[ \boxed{ a=\frac{\rho}{5}(\sqrt7+3\sqrt2\\,i), \qquad \rho>0. } \\]

Notice that the magnitude \\(\rho\\) can be any positive real number. Only the argument of \\(a\\) is fixed.

**Step 5: Find the corresponding value of&#x20;**\\(w\\)**.**

Since the straight line is tangent to the circle, the point of intersection \\(w\\) is the point of tangency.

The centre is

\\[ O=(0,5). \\]

The perpendicular distance from \\(O\\) to the tangent is \\(3\sqrt2\\).

The normal vector to the tangent line is

\\[ \mathbf n=(\cos\theta,-\sin\theta). \\]

The perpendicular projection of \\(O\\) onto the tangent line gives the point \\(T\\).

Since

\\[ O\cdot\mathbf n=-5\sin\theta, \\]

the position vector of \\(T\\) is

\\[ \overrightarrow{OT} =5\sin\theta(\cos\theta,-\sin\theta). \\]

Thus,

\\[ T= (0,5)+ (5\sin\theta\cos\theta,-5\sin^2\theta). \\]

Therefore,

\\[ u=5\sin\theta\cos\theta \\]

and

\\[ v=5-5\sin^2\theta =5\cos^2\theta. \\]

Substituting

\\[ \sin\theta=\frac{3\sqrt2}{5}, \qquad \cos\theta=\frac{\sqrt7}{5}, \\]

we obtain

\\[ u=5\left(\frac{3\sqrt2}{5}\right) \left(\frac{\sqrt7}{5}\right) =\frac{3\sqrt{14}}5 \\]

and

\\[ v=5\left(\frac{\sqrt7}{5}\right)^2 =\frac75. \\]

Hence,

\\[ \boxed{ w=\frac{3\sqrt{14}}5+\frac75i }. \\]

This is the unique point of tangency and therefore the unique complex number \\(w\\) satisfying both equations.

## **4. Final answers — examination answer summary**

For convenient reference, these are the results to present in your answer booklet.

| Part                      | Final answer                                                |
| ------------------------- | ----------------------------------------------------------- |
| (a) Cartesian equation    | \\(x^2+(y-5)^2=18\\)                                        |
| (a) Centre                | \\(\boxed{(0,5)}\\)                                         |
| (a) Radius                | \\(\boxed{3\sqrt2}\\)                                       |
| (b) Minimum argument      | \\(\boxed{\frac{3\pi}{4}-\sin^{-1}\left(\frac13\right)}\\)  |
| (c) All possible \\(a\\)  | \\(\boxed{a=\frac{\rho}{5}(\sqrt7+3\sqrt2\\,i),\ \rho>0}\\) |
| (c) Corresponding \\(w\\) | \\(\boxed{w=\frac{3\sqrt{14}}5+\frac75i}\\)                 |

## **5. Important examination techniques and marking considerations**

**Part (a) — 3 marks**

- Correct substitution \\(z=x+iy\\).
- Correct expansion and simplification of the modulus equation.
- Correct completion of the square, followed by the centre and radius.

**Part (b) — 2 marks**

- Recognise that the minimum argument corresponds to a tangent from the fixed point \\(A=(9,-4)\\) to the circle.
- Use the perpendicular radius and right-angled triangle to obtain the exact angle.

**Part (c) — 5 marks**

- Recognise that equal distances from \\(a^\*\\) and \\(-a^\*\\) give a perpendicular bisector.
- Derive the straight-line equation correctly.
- Interpret exactly one intersection as tangency.
- Use the perpendicular-distance formula to determine \\(\theta\\).
- Find the tangent point and express both \\(a\\) and \\(w\\) correctly.

**A particularly important distinction in part (c):**

Do not assume that \\(a\\) has a unique value. The question specifies its argument range, not its modulus. Consequently, there are infinitely many possible values of \\(a\\), all lying on the same ray from the origin. They all produce the same unique value of \\(w\\).

The solution above uses exact values throughout, with no calculator approximations required.

**Source verification:** The original examination question is on page 4 of your uploaded PDF.&#x20;

2026\_ Prelim_P1.pdf



**Overall conclusion:** The essential geometric insight is that part (b) involves tangents from an external point to a circle, while part (c) involves a perpendicular bisector becoming tangent to that same circle. Recognising these two geometric relationships makes the entire 10-mark question considerably more straightforward.
