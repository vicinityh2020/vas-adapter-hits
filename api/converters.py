from datetime import datetime
import random, string


class ReservationConverter:

    @staticmethod
    def seconds_to_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        hm_time = "%d:%02d" % (h, m)

        r = datetime.strptime(hm_time, '%H:%M').time()

        return r

    @staticmethod
    def generate_unique_res():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

