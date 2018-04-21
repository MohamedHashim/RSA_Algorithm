# RSA Algorithm
Simple implementation of RSA algorithm, asymmetric cryptography algorithm

 The concept of RSA Algorithm is generating public and private keys in 512 bits.
 
 ![Screenshot](https://github.com/MohamedHashim/RSA_Algorithm/master/screenshot.PNG)

 ### The Algorithm theory:
 
 #### 1-	Key Generation

•	Choose two random prime numbers p & q using Miller-Rabin Test <br />
•	Compute n =p*q <br />
•	Compute euler phi = (p-1) (q-1) <br />
•	Choose e, random prime number in specific range <br />
•	Then get the key of (n,e) <br />

 #### 2- Message Encryption using EEA (Extended Euclidean algorithm)

•	C = m^e mod n

 #### 3-	Message Decryption using CRT

•	C^d mod n<br />
•	e^-1 mod phi

 #### •	Miller-Rabin Test

1-	Get U & R from the prime number <br />
2-	Use Square and multiply algorithm to allow fast exponentiaition 

 #### •	CRT

1-	Modular representation of y into p and q  <br />
```
𝑦𝑝=𝑦 𝑚𝑜𝑑 𝑝 
𝑦𝑞=𝑦 𝑚𝑜𝑑 𝑞 
```
2-	Compute exponents  <br />

    𝑑𝑝=𝑑 𝑚𝑜𝑑 (𝑝−1) 
    𝑑𝑞=𝑑 𝑚𝑜𝑑 (𝑞−1) 

3-	Compute exponentiation <br />

    𝑥𝑝=𝑦𝑝𝑑𝑝 𝑚𝑜𝑑 𝑝
    𝑥𝑞=𝑦𝑞𝑑𝑞 𝑚𝑜𝑑 𝑞
    
4-	Compute C:  <br />

    𝐶𝑝=𝑞−1 𝑚𝑜𝑑 𝑝 
    𝐶𝑞=𝑝−1 𝑚𝑜𝑑 𝑞 

5-	Compute X  <br />

    𝑋 = {(𝑞.𝐶𝑝)𝑋𝑝 + (𝑝.𝐶𝑞) 𝑋𝑞} 𝑚𝑜𝑑 𝑛 

