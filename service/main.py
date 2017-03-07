import json
from os import path

from jnius import autoclass
import websocket

WS_SERVER = "ws://192.168.1.101:8282"
PATH_TO_CONF = path.abspath(path.join(path.dirname(__file__), '..', 'configuration.json'))

"""SOME JAVA SHIT"""

Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
AndroidString = autoclass('java.lang.String')
NotificationBuilder = autoclass('android.app.Notification$Builder')
PythonService = autoclass('org.renpy.android.PythonService')
service = PythonService.mService
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Drawable = autoclass("{}.R$drawable".format(service.getPackageName()))
notification_service = service.getSystemService(Context.NOTIFICATION_SERVICE)
icon = getattr(Drawable, 'icon')
notification_builder = NotificationBuilder(service)
java_class = service.getClass()

intent = Intent(service, PythonActivity)
intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP)

pendingIntent = PendingIntent.getActivity(service, 0, intent, 0)
notification_builder.setContentIntent(pendingIntent)

"""END OF SOME JAVA SHIT"""


def on_message(ws, message):
    print message
    title = AndroidString("Community".encode('utf-8'))
    _message = AndroidString(message.encode('utf-8'))

    notification_builder.setContentTitle(title)
    notification_builder.setContentText(_message)

    notification_builder.setSmallIcon(icon)
    notification_builder.setAutoCancel(True)
    notification_service.notify(0, notification_builder.build())


def on_error(ws, error):
    print error


def on_close(ws):
    print 'closed'


if __name__ == "__main__":

    with open(PATH_TO_CONF, 'r') as conf:
        user = json.load(conf)['user']
        payload = {
            'account': str(user.get('id')),
            'session': user.get('session')
        }
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        WS_SERVER,
        header=payload,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
