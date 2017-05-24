# In consumers.py
from channels import Group


# Connected to websocket.connect
def ws_add(message, user_id):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("message-updates-%s" % user_id).add(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message, user_id="blah"):
    Group("message-updates-%s" % user_id).discard(message.reply_channel)
