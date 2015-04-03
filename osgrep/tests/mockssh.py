from sshim.Server import Handler, Actor


class ExecHandler(Handler):

    def check_channel_exec_request(self, channel, command):
        channel.setblocking(True)
        Actor(self, channel).start()
        return True
