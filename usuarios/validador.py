# -*- coding: utf8 -*-
class Validador:
    TABLA_NIF = 'TRWAGMYFPDXBNJZSQVHLCKE'  # Valores para validar el NIF

    CLAVES_CIF = 'PQS' + 'ABEH' + 'CDFGJRUVNW'
    CLAVES_NIF1 = 'LKM'  # Son especiales, se validan
    # como CIFs
    CLAVES_NIF2 = 'XYZ'
    CLAVES_NIF = CLAVES_NIF1 + CLAVES_NIF2

    CONTROL_CIF_LETRA = 'KPQS'
    CONTROL_CIF_NUMERO = 'ABEH'

    EQUIVALENCIAS_CIF = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G',
                         8: 'H', 9: 'I', 10: 'J', 0: 'J'}

    def validarNIF(self, valor):
        """
        Nos indica si un NIF es valido.
        El valor debe estar normalizado
        @note:
          - ante cualquier problema se valida como False
        """
        bRet = False

        if len(valor) == 9:
            try:
                if valor[0] in self.__class__.CLAVES_NIF1:
                    bRet = self.validarCIF(valor)
                else:
                    num = None
                    if valor[0] in self.__class__.CLAVES_NIF2:
                        pos = self.__class__.CLAVES_NIF2.find(valor[0])
                        sNum = str(pos) + valor[1:-1]
                        num = int(sNum)
                    elif valor[0].isdigit():
                        num = int(valor[:-1])
                    if num != None and self.__class__.TABLA_NIF[num % 23] == valor[-1]:
                        bRet = True
            except:
                pass

        return bRet

    def validarCIF(self, valor):
        """
        Nos indica si un CIF es valido.
        El valor debe estar normalizado
        @note:
          - ante cualquier problema se valida como False
        """
        bRet = False

        if len(valor) == 9:
            v0 = valor[0]
            if v0 in self.__class__.CLAVES_NIF1 or v0 in self.__class__.CLAVES_CIF:
                try:
                    sumPar = 0
                    sumImpar = 0
                    for i in xrange(1, 8):
                        if i % 2:
                            v = int(valor[i]) * 2
                            if v > 9: v = 1 + (v - 10)
                            sumImpar += v
                        else:
                            v = int(valor[i])
                            sumPar += v
                    suma = sumPar + sumImpar
                    e = suma % 10
                    d = 10 - e
                    letraCif = self.__class__.EQUIVALENCIAS_CIF[d]
                    if valor[0] in self.__class__.CONTROL_CIF_LETRA:
                        if valor[-1] == letraCif: bRet = True
                    elif valor[0] in self.__class__.CONTROL_CIF_NUMERO:
                        if d == 10: d = 0
                        if valor[-1] == str(d): bRet = True
                    else:
                        if d == 10: d = 0
                        if valor[-1] == str(d) or valor[-1] == letraCif: bRet = True
                except:
                    pass

        return bRet

    def validar(self, valor):
        """
        Nos valida un CIF o un NIF
        """
        bRet = False

        if len(valor) == 9:
            if valor[0] in self.__class__.CLAVES_NIF or valor[0].isdigit():
                bRet = self.validarNIF(valor)
            else:
                bRet = self.validarCIF(valor)

        return bRet
