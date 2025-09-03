from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager

ORDER_MODE_RANDOMLY = 1
ORDER_MODE_ALTERNATIVELY = 2

class SoundPack(object):
    def __init__(self, mute_music, mute_percentage, order_mode, sounds):
        self.mute_music = mute_music
        self.mute_percentage = mute_percentage
        self.order_mode = order_mode
        self.sounds = sounds

    def __repr__(self):
        return "SoundPack {!r} order mode with {} sounds".format(self.order_mode, len(self.sounds))

class SoundEffectsManager(Manager):
    s_soundEffects = {}
    s_exclusion_funcs = {}
    s_lastSounds = {}

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            event = record.get("Event")
            mute_music = bool(record.get("MuteMusic", 0))
            mute_percentage = float(record.get("MutePercentage", 1.0))
            mode = record.get("OrderMode")
            sounds = record.get("Sounds")

            if event is None:
                Trace.log("Manager", 0, "SoundEffectsManager {!r}, no identity for record {!r}|{!r}|{!r}"
                          .format(param, event, mode, sounds))
                continue

            if len(sounds) == 0:
                Trace.log("Manager", 0, "SoundEffectsManager {!r}, {!r} record doesn't have any sound"
                          .format(param, event))
                continue

            for sound in sounds:
                if Mengine.hasSound(sound) is False:
                    Trace.log("Manager", 0, "SoundEffectsManager {!r} not found sound {!r} for event {!r}"
                              .format(param, sound, event))
                    continue

            sound_pack = SoundPack(mute_music, mute_percentage, mode, sounds)
            SoundEffectsManager.s_soundEffects[event] = sound_pack

        return True

    @staticmethod
    def addExclusion(identity, label, exclusion):
        SoundEffectsManager.s_exclusion_funcs.setdefault(identity, {})[label] = exclusion

    @staticmethod
    def getEventSounds():
        return SoundEffectsManager.s_soundEffects

    @staticmethod
    def getExclusionFuncs():
        return SoundEffectsManager.s_exclusion_funcs

    @staticmethod
    def setLastSound(identity, sound):
        SoundEffectsManager.s_lastSounds[identity] = sound

    @staticmethod
    def getLastSound(identity):
        return SoundEffectsManager.s_lastSounds.get(identity, None)

    @staticmethod
    def getEventSoundPack(identity):
        if identity not in SoundEffectsManager.s_soundEffects:
            Trace.log("Manager", 0, "Sound pack {!r} not found".format(identity))
            return None
        return SoundEffectsManager.s_soundEffects[identity]

    @staticmethod
    def getSingleSoundFromPack(identity):
        sound_pack = SoundEffectsManager.getEventSoundPack(identity)
        sound_pack_sounds = sound_pack.sounds
        sound = sound_pack_sounds[0]
        return sound

    @staticmethod
    def getRandomSoundFromPack(identity):
        sound_pack = SoundEffectsManager.getEventSoundPack(identity)
        sound_pack_sounds = sound_pack.sounds
        sound_number = Mengine.range_rand(0, len(sound_pack_sounds)) - 1
        sound = sound_pack_sounds[sound_number]
        return sound

    @staticmethod
    def getNextSoundFromPack(identity):
        sound_pack = SoundEffectsManager.getEventSoundPack(identity)
        sound_pack_sounds = sound_pack.sounds
        next_sound = sound_pack_sounds[0]

        sound_pack_len = len(sound_pack_sounds)
        if sound_pack_len == 1:
            return next_sound

        last_sound = SoundEffectsManager.getLastSound(identity)
        if last_sound is None:
            return next_sound

        last_sound_index = sound_pack_sounds.index(last_sound)
        if last_sound_index + 1 == sound_pack_len:
            return next_sound

        next_sound = sound_pack_sounds[last_sound_index + 1]
        return next_sound
