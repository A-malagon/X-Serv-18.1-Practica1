#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp


class AcortadorApp(webapp.webApp):

    def __init__(self, hostname, port):
        self.name = hostname
        self.port = str(port)
        self.urlReal = {}
        self.urlCorta = {}
        self.cortaEncontrada = 0
        webapp.webApp.__init__(self, hostname, port)

    def acortarURL(self, url):
        if url.find("%3A%2F%2F") == -1:
            url = "http://" + url
        else:
            url = url.split("%3A%2F%2F")[1]
            url = "http://" + url
        return url

    def pedirFormulario(self):
        formulario = '<form action="" method="POST" accept-charset="UTF-8">' +\
                     'Acorta url: <input type="text" name="url">' +\
                     '<input type="submit" value="Enviar"></form>'
        return formulario

    def cuerpoMetodo(self, metodo, request):
        if metodo == "GET":
            cuerpo = ""
        elif metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[-1]
            cuerpo = cuerpo.split('=')[1]
        return cuerpo

    def parse(self, request):

        metodo = request.split(" ")[0]
        recurso = request.split(" ")[1]
        cuerpo = self.cuerpoMetodo(metodo, request)
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
                recurso = recurso.split('/')[1]
                if recurso in self.urlCorta:
                    url = self.urlCorta[recurso]
                    print "Redireccionando a la URL " + url
                    httpCode = "300 Redirect"
                    htmlBody = "<html><body><meta http-equiv='refresh'\
                                content='0; \
                                URL=" + url + "'></body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body><h1>Recurso no disponible</h1>\
                                </body></html>"
            return httpCode, htmlBody
        elif metodo == "POST":
            url = cuerpo
            if url == "":
                httpCode = "400 Error"
                htmlBody = "<html><body><h1>Error:Post vacio</h1>\
                            </body></html>"
                return httpCode, htmlBody
            url = self.acortarURL(url)
            print "URL:" + url
            if url in self.urlReal:
                cortaEncontrada = self.urlReal[url]
            else:
                cortaEncontrada = "http://" + self.name + ":" + \
                                  self.port + "/" + \
                                  str(self.cortaEncontrada)
                self.urlReal[url] = cortaEncontrada
                self.urlCorta[str(self.cortaEncontrada)] = url
                self.cortaEncontrada += 1
            httpCode = "200 OK"
            htmlBody = "<html><body><p>url real: <a href=" +\
                       url + ">" + url + \
                       "</a></p>url acortada: <a href=" +\
                       cortaEncontrada + ">" + cortaEncontrada +\
                       "<body text='red'>" +\
                       "<body bgcolor='#000000'>" +\
                       "</a></body></html>"
            return httpCode, htmlBody
        else:
            httpCode = "400 Error"
            htmlBody = "<html><body><h1>Ni POST ni GET</h1></body></html>"
        return httpCode, htmlBody

if __name__ == "__main__":
    try:
        Servidor = AcortadorApp("localhost", 1234)
    except KeyboardInterrupt:
        print "\nCerrando el servidor\n"
    except TypeError:
        print "host name[string]  port[int]"
