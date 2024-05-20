from Foundation.System import System
from MobileKit.SoundEffectsManager import SoundEffectsManager
from MobileKit.SoundEffectsManager import ORDER_MODE_RANDOMLY, ORDER_MODE_ALTERNATIVELY


class SystemSoundEffects(System):

    def _onParams(self, params):
        super(SystemSoundEffects, self)._onParams(params)
        self.sound_events = []

    def _onRun(self):
        self.sound_events = SoundEffectsManager.getEventSounds()
        for identity, sound_pack in self.sound_events.items():
            self.addSoundObserver(identity, sound_pack)

        return True

    def _onStop(self):
        self.sound_events = []

    def addSoundObserver(self, identity, sound_pack):
        def __cbSoundPlay(*args):
            """
            callback from observer to play sound
            """
            def __cbSoundPlayEnd(play, callback=None):
                """
                callback when sound end play to unmute music
                """
                if callback == 0:
                    return
                if sound_play.getId() != play.getId():
                    return

                if music_volume > 0.0 and sound_pack.mute_percentage < 1.0:
                    Mengine.musicSetVolumeTag(identity, music_volume, mute_value)

            # Check for exclusions to play sound
            if self.shouldSkip(identity, *args) is True:
                return False

            # Get sound by checking order mode
            if sound_pack.order_mode is None:
                sound = SoundEffectsManager.getSingleSoundFromPack(identity)
            elif sound_pack.order_mode == ORDER_MODE_RANDOMLY:
                sound = SoundEffectsManager.getRandomSoundFromPack(identity)
            elif sound_pack.order_mode == ORDER_MODE_ALTERNATIVELY:
                sound = SoundEffectsManager.getNextSoundFromPack(identity)
            else:
                Trace.log("System", 0, "Sound by order mode {!r} not found".format(sound_pack.order_mode))
                return False

            # Remember that sound as last played
            SoundEffectsManager.setLastSound(identity, sound)

            # Check if sound should mute music
            if sound_pack.mute_music is False:
                Mengine.soundPlay(sound, False, None)
            elif sound_pack.mute_music is True:
                music_volume = Mengine.musicGetVolume()

                if music_volume > 0.0 and sound_pack.mute_percentage < 1.0:
                    mute_value = music_volume * sound_pack.mute_percentage
                    Mengine.musicSetVolumeTag(identity, mute_value, music_volume)

                sound_play = Mengine.soundPlay(sound, False, __cbSoundPlayEnd)

            return False

        notificator = Notificator.getIdentity(identity)
        self.addObserver(notificator, __cbSoundPlay)

    def shouldSkip(self, identity, *args):
        exclusion_funcs = SoundEffectsManager.getExclusionFuncs()

        if identity not in exclusion_funcs:
            return False

        for func in exclusion_funcs[identity].itervalues():
            if func(*args) is True:
                return True

        return False
