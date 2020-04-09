listaUsuarios = []
async def websocket_application(scope, receive, send):
    
    while True:
        event = await receive()
        #print(scope)
        if event['type'] == 'websocket.connect':
            if scope['client'] not in listaUsuarios:
                listaUsuarios.append(scope['client'])
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            listaUsuarios.remove(scope['client'])
            print(listaUsuarios)
            break

        if event['type'] == 'websocket.receive':
            print(scope['client'])
            print(listaUsuarios)
            print(scope)
            if event['text'] == 'ping':
                await send({
                    'type': 'websocket.send',
                    'text': 'pong!'
                })