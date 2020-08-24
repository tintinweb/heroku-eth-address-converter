import os
from flask import Flask, request, redirect, render_template

import urllib.parse

from eth_keys import keys
from p2p.kademlia import Address, Node
from p2p.kademlia import Node as KNode

from p2p.enr import ENR
import base58
import base64
import multiaddr

class Handler:

    @staticmethod
    def enodeToMultiAddress(_node):
        u = urllib.parse.urlparse(_node)
        pubkey =  bytearray.fromhex(u.username)
        xpub = keys.PublicKey(pubkey)
        nn = Node.from_pubkey_and_addr(xpub, Address(u.hostname, u.port, u.port)) 
        nodeid = base58.b58encode(nn.id)
        return multiaddr.Multiaddr("/ip4/"+u.hostname+"/tcp/"+str(u.port)+"/p2p/"+nodeid.decode("utf-8") )


    @staticmethod
    def enrToMultiAddress(_enr):
        knode = KNode.from_enr_repr(_enr)
        return {"enode": knode.uri(),
                "multiaddr": Handler.enodeToMultiAddress(knode.uri())} 

    @staticmethod
    def convertAll(_node):

        ret = {
            "enode":"",
            "enr":"",
            "multiaddr":""
        }

        if(_node.startswith("/")):
            ret["multiaddr"] = multiaddr.Multiaddr(_node)
        elif(_node.startswith("enode://")):
            ret["enode"] = _node
            ret["multiaddr"] = Handler.enodeToMultiAddress(_node)
        elif(_node.startswith("enr:")):
            ret["enr"] = _node
            ret.update(Handler.enrToMultiAddress(_node))

        print(ret)
        return ret
    
    @staticmethod
    def render(inaddress):
        return Handler.convertAll(inaddress)

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

# controllers
@app.route("/")
def hello():
    inaddr = request.args.get('inaddr') 
    if inaddr:
        inaddr = urllib.parse.unquote(inaddr)
        return render_template('index.html', data=Handler.render(inaddr))
    return render_template('index.html')




# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)