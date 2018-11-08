import sys
import os
import platform
import json
import time
import ctypes


#Class that defines a various methods to interact with Emotiv Insight
class Insight(object):
    #self is always use as first parameter for instance method, Python sends instance along with method call
    #self allows python to know which object is being called and whose instance attributes to update
    #Method, _init_ means initialization, all of these variables are initialized upon calling this method
    def __init__(self, composerConnect=False, composerPort=1726, userID=0):
        #libEDK = cdll.LoadLibrary("edk.dll")# this is the problem here
        self.composerConnect = composerConnect#Sets boolean variable composerConnect to True or False
        self.composerPort = composerPort#Sets composerPort varaible to 1726 or other value
        self.userID = ctypes.c_uint(userID)#c_unit means unsigned integer
        self.user = ctypes.pointer(self.userID)#Creates and returns new ctypes pointer type

        self.FE_SURPRISE = 64#initializes values, not sure what they mean 
        self.FE_FROWN = 32
        self.FE_SMILE = 128
        self.FE_CLENCH = 256
        self.FacialExpressionStates = {}
        self.FacialExpressionStates[self.FE_FROWN] = 0
        self.FacialExpressionStates[self.FE_SURPRISE] = 0
        self.FacialExpressionStates[self.FE_SMILE] = 0
        self.FacialExpressionStates[self.FE_CLENCH] = 0
        try:
            if sys.platform.startswith('win32'):#If running on windowns, loads this foreign library
                self.libEDK = ctypes.cdll.LoadLibrary("edk.dll")
            if sys.platform.startswith('linux'):
                srcDir = os.getcwd()
                libPath = srcDir + "/libedk.so"
                self.libEDK = ctypes.CDLL(libPath)
        except:
            print ('Error : cannot load dll lib')

        IEE_EmoEngineEventCreate = self.libEDK.IEE_EmoEngineEventCreate
        IEE_EmoEngineEventCreate.restype = ctypes.c_void_p
        self.eEvent = IEE_EmoEngineEventCreate()

        IEE_EmoStateCreate = self.libEDK.IEE_EmoStateCreate
        IEE_EmoStateCreate.restype = ctypes.c_void_p
        self.eState = IEE_EmoStateCreate()
    # The following methods use the library loaded in the initialization
    def disconnect(self):
        self.libEDK.IEE_EngineDisconnect()
        self.libEDK.IEE_EmoStateFree(eState)
        self.libEDK.IEE_EmoEngineEventFree(eEvent)

    def connect(self):
        if self.composerConnect:
            self.libEDK.IEE_EngineRemoteConnect("127.0.0.1", self.composerPort)#Start listening on this port (1726)
            if self.libEDK.IEE_EngineRemoteConnect("127.0.0.1", self.composerPort) != 0:
                print ("Cannot connect to EmoComposer on")
        else:
            self.libEDK.IEE_EngineConnect("Emotiv Systems-5")

    def get_state(self, eEvent):
        return self.libEDK.IEE_EngineGetNextEvent(eEvent)

    def get_event_type(self, eEvent):
        return self.libEDK.IEE_EmoEngineEventGetType(eEvent)

    def get_engine_event_emo_state(self, eEvent, eState):
        IEE_EmoEngineEventGetEmoState = \
            self.libEDK.IEE_EmoEngineEventGetEmoState
        IEE_EmoEngineEventGetEmoState.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p]
        IEE_EmoEngineEventGetEmoState.restype = ctypes.c_int
        return IEE_EmoEngineEventGetEmoState(eEvent, eState)

    def get_userID(self, eEvent, user):
        return self.libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)

    def get_time_from_start(self, eState):
        IS_GetTimeFromStart = self.libEDK.IS_GetTimeFromStart
        IS_GetTimeFromStart.argtypes = [ctypes.c_void_p]
        IS_GetTimeFromStart.restype = ctypes.c_float
        return IS_GetTimeFromStart(eState)

    def get_wireless_signal_status(self, eState):
        IS_GetWirelessSignalStatus = self.libEDK.IS_GetWirelessSignalStatus
        IS_GetWirelessSignalStatus.restype = ctypes.c_int
        IS_GetWirelessSignalStatus.argtypes = [ctypes.c_void_p]
        return IS_GetWirelessSignalStatus(eState)

    def get_facial_expression_is_blink(self, eState):
        IS_FacialExpressionIsBlink = self.libEDK.IS_FacialExpressionIsBlink
        IS_FacialExpressionIsBlink.restype = ctypes.c_int
        IS_FacialExpressionIsBlink.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionIsBlink(eState)

    def get_left_wink(self, eState):
        IS_FacialExpressionIsLeftWink = \
            self.libEDK.IS_FacialExpressionIsLeftWink
        IS_FacialExpressionIsLeftWink.restype = ctypes.c_int
        IS_FacialExpressionIsLeftWink.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionIsLeftWink(eState)

    def get_right_wink(self, eState):
        IS_FacialExpressionIsRightWink = \
            self.libEDK.IS_FacialExpressionIsRightWink
        IS_FacialExpressionIsRightWink.restype = ctypes.c_int
        IS_FacialExpressionIsRightWink.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionIsRightWink(eState)

    def get_upper_face_action(self, eState):
        IS_FacialExpressionGetUpperFaceAction =  \
            self.libEDK.IS_FacialExpressionGetUpperFaceAction
        IS_FacialExpressionGetUpperFaceAction.restype = ctypes.c_int
        IS_FacialExpressionGetUpperFaceAction.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionGetUpperFaceAction(eState)

    def get_upper_face_action_power(self, eState):
        IS_FacialExpressionGetUpperFaceActionPower = \
            self.libEDK.IS_FacialExpressionGetUpperFaceActionPower
        IS_FacialExpressionGetUpperFaceActionPower.restype = ctypes.c_float
        IS_FacialExpressionGetUpperFaceActionPower.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionGetUpperFaceActionPower(eState)

    def get_lower_face_action(self, eState):
        IS_FacialExpressionGetLowerFaceAction = \
            self.libEDK.IS_FacialExpressionGetLowerFaceAction
        IS_FacialExpressionGetLowerFaceAction.restype = ctypes.c_int
        IS_FacialExpressionGetLowerFaceAction.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionGetLowerFaceAction(eState)

    def get_lower_face_action_power(self, eState):
        IS_FacialExpressionGetLowerFaceActionPower = \
            self.libEDK.IS_FacialExpressionGetLowerFaceActionPower
        IS_FacialExpressionGetLowerFaceActionPower.restype = ctypes.c_float
        IS_FacialExpressionGetLowerFaceActionPower.argtypes = [ctypes.c_void_p]
        return IS_FacialExpressionGetLowerFaceActionPower(eState)

    def get_mental_command_current_action(self, eState):
        IS_MentalCommandGetCurrentAction = \
            self.libEDK.IS_MentalCommandGetCurrentAction
        IS_MentalCommandGetCurrentAction.restype = ctypes.c_int
        IS_MentalCommandGetCurrentAction.argtypes = [ctypes.c_void_p]
        return IS_MentalCommandGetCurrentAction(eState)

    def get_mental_command_current_action_power(self, eState):
        IS_MentalCommandGetCurrentActionPower = \
            self.libEDK.IS_MentalCommandGetCurrentActionPower
        IS_MentalCommandGetCurrentActionPower.restype = ctypes.c_float
        IS_MentalCommandGetCurrentActionPower.argtypes = [ctypes.c_void_p]
        return IS_MentalCommandGetCurrentActionPower(eState)

    def lower_facial_expression_states(self, eState):
        lower_face_action = self.get_lower_face_action(eState)
        lower_face_action_power = self.get_lower_face_action_power(eState)
        self.FacialExpressionStates[lower_face_action] = lower_face_action_power

    def upper_facial_expression_states(self, eState):
        self.upper_face_action = self.get_upper_face_action(eState)
        self.upper_face_action_power = self.get_upper_face_action_power(eState)
        self.FacialExpressionStates[self.upper_face_action] = self.upper_face_action_power

    def get_surprise(self, eState):
        self.upper_facial_expression_states(eState)
        return self.FacialExpressionStates[self.FE_SURPRISE]

    def get_frown(self, eState):
        self.upper_facial_expression_states(eState)
        return self.FacialExpressionStates[self.FE_FROWN]

    def get_smile(self, eState):
        self.lower_facial_expression_states(eState)
        return self.FacialExpressionStates[self.FE_SMILE]

    def get_clench(self, eState):
        self.lower_facial_expression_states(eState)
        return self.FacialExpressionStates[self.FE_CLENCH]

