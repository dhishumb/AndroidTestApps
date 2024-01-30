
import  uvicorn
import os

if __name__ == '__main__':
    print(os.getcwd())
    keyfile = os.path.join(os.getcwd(),'ssl','ct-test.us.bank-dns.com.key')
    certfile = os.path.join(os.getcwd(),'ssl','ct-test.us.bank-dns.com.crt')
    uvicorn.run("app.main:app",host="ct-test.us.bank-dns.com",port=30050,reload=True,ssl_keyfile=keyfile, ssl_certfile=certfile)