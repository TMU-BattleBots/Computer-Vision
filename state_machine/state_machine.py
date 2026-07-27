"""
Core state machine implementation.

This module defines the main StateMachine class that manages state
transitions and executes state-specific behaviors. Orchestrates
the high-level battlebot strategy based on perception inputs.
"""
from interfaces.detector_interface import DetectionResult
from state_machine.states import RobotState

class StateMachine:
    """
    Robot Behaviour
    Flow: 
        INIT -> SEARCH -> TRACK -> CHASE -> LOST -> SEARCH 
    """
    
    def __init__(self):
        self.state = RobotState.INIT

        # To avoid reacting to one bad frame
        self.track_counter = 0

        # Used for when target is not to be found
        self.lost_counter = 0


    def update(self, detection: DetectionResult) -> RobotState:
        """
        Update robot state based on current detection result.
        """

        if self.state == RobotState.INIT:
            self.state = RobotState.SEARCH


        elif self.state == RobotState.SEARCH:

            if detection.target_visible:
                self.track_counter += 1

                # Multiple frames before trusting detection
                if self.track_counter >= 3:
                    self.state = RobotState.TRACK
                
            else:
                self.track_counter = 0
                
        elif self.state == RobotState.TRACK:

            if detection.target_visible:
                self.track_counter += 1

                if self.track_counter >= 5:
                    self.state = RobotState.CHASE

            else:
                self.track_counter = 0
                self.state = RobotState.SEARCH


        elif self.state == RobotState.CHASE:

            if not detection.target_visible:
                self.lost_counter = 0
                self.state = RobotState.LOST


        elif self.state == RobotState.LOST:

            self.lost_counter += 1

            if detection.target_visible:
                self.lost_counter = 0
                self.state = RobotState.CHASE
                
            elif self.lost_counter >= 15:
                self.lost_counter = 0
                self.state = RobotState.SEARCH


        return self.state