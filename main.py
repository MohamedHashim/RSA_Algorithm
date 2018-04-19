from random import randrange
from tkinter import *

def get_u_r(num):
    u = 0
    num -= 1

    while True:
        u += 1
        num //= 2
        if u != 0 and num % 2 != 0:
            break

    return (u, num)

def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return 0
    # Assert :: (modulus - 1) * (modulus - 1) does not overflow base
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def miller_rabin(p, s):
    if p == 2:
        return True
    if p % 2 == 0:
        return False

    u, r = get_u_r(p)
    for i in range(s):
        a = randrange(2, p - 1)
        z = modular_pow(a, r, p)

        if z != 1 and z != (p - 1):
            for j in range(u):
                z = modular_pow(z, 2, p)
                if z == p - 1:
                    break
            else:
                return False

    return True

def get_rand_prime(nbits=16):
    while True:
        p = randrange(2 ** nbits, 2 * 2 ** nbits)
        # print(p)
        if miller_rabin(p, 100):
            return p

def inverse(ra, rb):
    if rb > ra:
        ra, rb = rb, ra

    modulos = ra
    mult = [(1, 0), (0, 1)]
    i = 2
    while True:
        # print(str(ra) + " = " + str(rb) + "*", end='')
        mod = ra % rb
        q = (ra - mod) // rb
        # print(str(q)+" + " + str(mod))
        ra = rb
        rb = mod
        mult = [
            (mult[1][0], mult[1][1]),
            ((-q * mult[1][0]) + mult[0][0], (-q * mult[1][1]) + mult[0][1])
        ]
        if mod == 0:
            # print("GCD = " + str(ra))
            if ra == 1:
                return mult[0][1] % modulos
            else:
                return -1
            break
        # else:
        # print("R" + str(i) + " = " + str(mult[1][0]) + " * R" + str(i-2) + " + " + str(mult[1][1]) + " * R" + str(i-1))

def CRT(y, d, p, q):
    n = p * q

    # 1- Convert to CRT domain
    yp = y % p
    yq = y % q
    # print("(yp, yq) = ", str((yp, yq)))

    # 2- Do the computations
    dp = d % (p - 1)
    dq = d % (q - 1)
    # print("(dp, dq) = ", str((dp, dq)))

    xp = pow(yp, dp, p)
    xq = pow(yq, dq, q)
    # print("(xp, xq) = ", str((xp, xq)))

    # 3- Inverse transform
    inv = inverse(p, q)
    print(inv)
    cp = pow(q, p - 2, p)
    cq = pow(p, q - 2, q)
    # print(cq == pow(p, q-2, q))
    # print("(cp, cq) = ", str((p, q)))

    x = ((q * cp * xp) + (p * cq * xq)) % n
    # print("x = ", x, "mod " + str(n))
    return x

def msg_to_int(msg):
    int_msg = ""
    for ch in msg:
        pre = "{0:b}".format(ord(ch))
        if len(pre) < 7:
            pre = "0" * (7 - len(pre)) + pre
        int_msg += pre

    return int(int_msg, 2)

def int_to_msg(i):
    bin_format = "{0:7b}".format(i)
    msg = ""

    for b in range(0, len(bin_format), 7):
        msg += chr(int(bin_format[b:b + 7], 2))

    return msg


def encryption(msg, e, n):
    int_msg = msg_to_int(msg)
    encrypted = modular_pow(int_msg, e, n)
    # print(setuptime + '\n Encrypted Message = ', encrypted)
    return encrypted


def decryption(msg, d, p, q):
    decrypted = CRT(int(msg), d, p, q)
    # print('\nMessage = ', int_to_msg(decrypted))
    return int_to_msg(decrypted)


def RSA_Init(nbits=512):  # setup
    p = get_rand_prime(nbits)
    q = get_rand_prime(nbits)
    while p == q:
        q = get_rand_prime(nbits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = randrange(2 ** 16, 2 ** 17)
    d = inverse(phi, e)
    while d == -1:
        e = randrange(2 ** 16, 2 ** 17)
        d = inverse(phi, e)

    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d
    }


RSAparams = RSA_Init(512)  

root = Tk()

actions_frame = Frame(root)
input_frame = Frame(root)
output_frame = Frame(root)

input_label = Label(input_frame, text="Input: ")
input_msg = Text(input_frame, height=4, width=128)

output_label = Label(output_frame, text="Output: ")
output_msg = Text(output_frame, height=4, width=128)

encrypt = Button(actions_frame, text="Encrypt", command=lambda: output_msg.insert("0.0", encryption(
    input_msg.get("0.0", "128.4").strip(), RSAparams['e'], RSAparams['n'])))
decrypt = Button(actions_frame, text="Decrypt", command=lambda: output_msg.insert("0.0", (decryption(
    input_msg.get("0.0", "128.4").strip(), RSAparams['d'], RSAparams['p'], RSAparams['q']))))


input_label.pack(side=LEFT)
input_msg.pack(side=LEFT)

encrypt.pack(side=LEFT)
decrypt.pack(side=LEFT)

output_label.pack(side=LEFT)
output_msg.pack(side=LEFT)

input_frame.pack()
actions_frame.pack()
output_frame.pack()

root.mainloop()
