from Cocoa import NSObject
import objc


class MacOSNotification(NSObject):
    def init(self):
        self.NSUserNotification = objc.lookUpClass('NSUserNotification')
        self.NSUserNotificationCenter = objc.lookUpClass(
            'NSUserNotificationCenter')
        return self

    def clearNotifications(self):
        self.NSUserNotificationCenter.defaultUserNotificationCenter(
        ).removeAllDeliveredNotifications()

    def notify(self, display_information={}, displayed_notification_buttons={}):
        notification = self.NSUserNotification.alloc().init()

        if 'title' in display_information:
            notification.setTitle_(str(display_information['title']))

        if 'subtitle' in display_information:
            notification.setSubtitle_(str(display_information['subtitle']))

        if 'informative_text' in display_information:
            notification.setInformativeText_(
                str(display_information['informative_text']))

        # if 'content_image' in display_information:
        #     notification.setContentImage_(str(display_information['content_image']))

        if 'sound_name' in display_information:
            notification.setSoundName_(str(display_information['sound_name']))
        else:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")

        notification.setHasActionButton_(False)
        notification.setActionButtonTitle_("View")

        self.NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
        self.NSUserNotificationCenter.defaultUserNotificationCenter(
        ).scheduleNotification_(notification)
        return notification

    def userNotificationCenter_shouldPresentNotification_(self, center, notification):
        return True


def main():
    # Objective C must allocate the space as shown in section "Object Creation" of http://zqpythonic.qiniucdn.com/data/20100625162918/index.html
    mac_os_notification = MacOSNotification.alloc().init()
    mac_os_notification.clearNotifications()

    display_information = {
        'title': 'Test Notification',
        'subtitle': 'test',
        'informative_text': 'test',
        'content_image': None,
        'identifier': '',
        'response': None,
        'responsePlaceholder': ''
    }

    displayed_notification_buttons = {
        'has_action_button': False,
        'action_button_title': '',
        'other_button_title': '',
        'has_reply_button': ''
    }

    notification = mac_os_notification.notify(
        display_information=display_information, displayed_notification_buttons=displayed_notification_buttons)


main()
