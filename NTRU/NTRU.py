from . import poly

class NTRU:
    def __init__(self, N, p, q, f, g):
        self.N= N
        self.p = p
        self.q = q
        self.f = f
        self.g = g

        print("Public ve Private anahtarlar oluşturuluyor")
        print("kullanılan değerler:")
        print(" N=", N)
        print(" p=", p)
        print(" q=", q)
        print("---------")
        print("Gönderenin polinomları (g,f):")
        print(" f(x)=", f)
        print(" g(x)=", g)

    def gen_keys(self):
        D = [0] * (self.N + 1)
        D[0] = -1
        D[self.N] = 1

        print("\nF_p ve F_q değerleri")
        [gcd_f, s_f, t_f] = poly.extEuclidPoly(self.f, D)

        self.f_p = poly.modPoly(s_f, self.p)
        self.f_q = poly.modPoly(s_f, self.q)

        print("F_p:", self.f_p)
        print("F_q:", self.f_q)

        x = poly.multPoly(self.f_q, self.g)
        self.h = poly.reModulo(x, D, self.q)

    def get_pubkey(self):
        return self.h

    def get_privkeys(self):
        return self.f, self.f_p

def encrypt(message, p, q, D, h):
    print("Orijinal mesaj:", message)
    msg1 = list(message)
    for i in range(len(msg1)):
        msg1[i] = ord(msg1[i])
    print(msg1)

    randPol = [-1, -1, 1, 1]
    encmsg = []
    l = []

    for i in msg1:
        print('----', i, '----')
        msg = poly.DecimalToBinary(i)

        print("Gönderenin mesajı:\t", msg)
        l.append(len(msg))
        print("Rastgele seçilen değer:\t\t\t", randPol)
        e_tilda = poly.addPoly(poly.multPoly(poly.multPoly([p], randPol),h), msg)
        e = poly.reModulo(e_tilda, D, q)
        encmsg.append(e)
        print("Şifrelenmiş mesaj:\t", e)

    print('\n\nenc', encmsg)

    return encmsg, l

def decrypt(encmsg, f, f_p, p, q, D, l):
    decmsg = []
    j = 0
    for e in encmsg:
        tmp = poly.reModulo(poly.multPoly(f, e), D, q)
        centered = poly.cenPoly(tmp, q)
        m1 = poly.multPoly(f_p, centered)
        tmp = poly.reModulo(m1, D, p)

        print("Çözümlenmiş Mesaj:\t", tmp[:l[j]])
        decmsg.append(tmp[:l[j]])
        j = j + 1

    print('dec', decmsg)
    fm = []
    print("\n\n--şifreleme--")
    for i in decmsg:
        decmsgpart = poly.binaryToDecimal(int(''.join(list(map(str, i)))))
        print(i, decmsgpart)
        fm.append(decmsgpart)
    print("\n\n")
    print('mesaj:\n\n', ''.join(list(map(chr, fm))))
    message = ''.join(list(map(chr, fm)))

    return message

