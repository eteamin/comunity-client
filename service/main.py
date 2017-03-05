# import json
#
# from plyer.platforms.android.notification import AndroidNotification
# import websocket
#
# from variables import WS_SERVER, PATH_TO_CONF
#
#
# def on_message(ws, message):
#     n = AndroidNotification()
#     n.notify(title=message)
#
#
# def on_error(ws, error):
#     pass
#
#
# def on_close(ws):
#     pass
#
#
# if __name__ == "__main__":
#     with open(PATH_TO_CONF, 'r') as conf:
#         user = json.load(conf)['user']
#         payload = {
#             'account': str(user.get('id')),
#             'session': user.get('session')
#         }
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(
#         WS_SERVER,
#         header=payload,
#         on_message=on_message,
#         on_error=on_error,
#         on_close=on_close
#     )
#     ws.run_forever()
