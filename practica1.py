#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp
import urllib
import socket


class acortaApp(webapp.webApp):
    CortaEncontrada = -1
    urlReal = {}
    urlCorta = {}

    def pedirFormulario(self):
        formulario = '<form action="" method="POST" accept-charset="UTF-8">' +\
                     'Acorta url: <input type="text" name="url">' +\
                     '<input type="submit" value="Enviar"></form>'
        return formulario

    def acortarURL(self, cuerpo):
        if cuerpo.find("http") == -1:
            cuerpo = "http://" + cuerpo
        else:
            cuerpo = cuerpo.replace('%3A%2F%2F', '://')
        return cuerpo

    def cuerpoMetodo(self, metodo, request):
        if metodo == "GET":
            cuerpo = ""
        elif metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[1].split('=')[1]
            cuerpo = cuerpo.replace('+', '')
        return cuerpo

    def parse(self, request):

        metodo = request.split(" ")[0]
        recurso = request.split(" ")[1]
        cuerpo = self.cuerpoMetodo(metodo, request)
        print metodo
        print recurso
        print cuerpo
        return (metodo, recurso, cuerpo)

    def process(self, parsedRequest):
        (metodo, recurso, cuerpo) = parsedRequest

        formulario = self.pedirFormulario()

        if metodo == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = ("<html><body>" + str(self.urlReal) +
                            formulario + "</body></html>")
            else:
                recurso = int(recurso.split('/')[1])
                if recurso[1:] in self.urlCorta:
                    httpCode = ("300 Redirect\nLocation: " +
                                self.urlCorta[recurso])
                    htmlBody = "<html><body>Redireccion</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = ("<html><body> Error:Recurso no disponible" +
                                "</body></html>")

        elif metodo == "POST":

            if cuerpo == "":
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>Error</body></html>")
                return (httpCode, htmlBody)
            else:
                cuerpo = self.acortarURL(cuerpo)

            if cuerpo in self.urlReal:
                self.CortaEncontrada = self.urlReal[cuerpo]
            else:
                self.CortaEncontrada = self.CortaEncontrada + 1
                self.urlReal[cuerpo] = self.CortaEncontrada
                self.urlCorta[self.CortaEncontrada] = cuerpo
                print self.CortaEncontrada

            httpCode = "200 OK"
            larga = "<a href ='" + cuerpo + "'> Url larga: " + cuerpo + "</a>"
            corta = ("<a href ='http://" + str(socket.gethostname()) +
                     ":1234/" + str(self.CortaEncontrada) +
                     "'> Url acortada : " + str(self.CortaEncontrada) + "</a>")
            htmlBody = ("<html><body> URLS: </br>" + larga + "</br>" +
                        corta + "</br>" + "</body></html>")
        return (httpCode, htmlBody)


if __name__ == '__main__':
    try:
        testacortador = acortaApp(socket.gethostname(), 1234)
    except KeyboardInterrupt:
        print "\nCerrando el servidor\n"
