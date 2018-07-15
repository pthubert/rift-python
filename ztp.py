import common.constants

class Ztp:

    ZTP_MIN_NUMBER_OF_PEER_FOR_LEVEL = 3

    @enum.unique
    class State(enum.Enum):
        UPDATING_CLIENTS = 1
        HOLDING_DOWN = 2
        COMPUTE_BEST_OFFER = 3

    @enum.unique
    class Event(enum.Enum):
        CHANGE_LOCAL_LEAF_INDICATIONS = 1
        CHANGE_LOCAL_CONFIGURED_LEVEL = 2
        NEIGHBOR_OFFER = 3
        WITH_DRAW_NEIGHBOROFFER = 4
        BETTER_HAL = 5
        BETTER_HAT = 6
        LOST_HAL = 7
        LOST_HAT = 8
        COMPUTATION_DONE = 9
        HOLDDOWN_EXPIRED = 10
        SHORT_TICK_TIMER = 11

    # on  LOST_HAT in ComputeBestOffer finishes in ComputeBestOffer:  LEVEL_COMPUTE
    # on    NeighborOffer in ComputeBestOffer    finishes in ComputeBestOffer: action_update_or_remove_offer
    #     if NeighborOffer.no_level_offered
    #           then REMOVE_OFFER
    #           else  if level > leaf
    #                   then UPDATE_OFFER
    #                   else REMOVE_OFFER
    # on    BetterHAL in ComputeBestOffer    finishes in ComputeBestOffer:    LEVEL_COMPUTE
    # on    ShortTic in COMPUTE_BEST_OFFER    finishes in COMPUTE_BEST_OFFER:
    # on BetterHAT in ComputeBestOffer finishes in ComputeBestOffer: LEVEL_COMPUTE
    # on WithdrawNeighborOffer in ComputeBestOffer finishes in ComputeBestOffer: REMOVE_OFFER
    # on ChangeLocalLeafIndications in ComputeBestOffer finishes in   ComputeBestOffer: action_store_leaf_flag,action_level_compute
    # on ComputationDone in ComputeBestOffer    finishes in    UpdatingClients: NO_ACTION
    # on ChangeLocalConfiguredLevel in ComputeBestOffer finishes in ComputeBestOffer:  action_store_level, action_level_compute
    # on LostHAL in ComputeBestOffer finishes in HoldingDown: action_update_holddown_timer_on_lost_hal
    #     if any    southbound    adjacencies    present
    #         then     update    holddown    timer    to    normal duration
    #         else fire holddown timer immediately


    # on  LOST_HAT  in                  HOLDING_DOWN   finishes in  HOLDING_DOWN:   NO_ACTION
    # on  LOST_HAL  in                  HOLDING_DOWN   finishes in  HOLDING_DOWN:   NO_ACTION
    # on  BETTER_HAT in                 HOLDING_DOWN   finishes in  HoldingDown:    NO_ACTION
    # on  ChangeLocalConfiguredLevel in HOLDING_DOWN   finishes in  ComputeBestOffer: STORE_LEVEL
    # on  HoldDownExpired in            HOLDING_DOWN   inishes in   ComputeBestOffer:    PURGE_OFFERS
    # on  ShortTic in                   HOLDING_DOWN   finishes in  HOLDING_DOWN:   action_check_hold_time_expired
    #    if HOLDDOWN_TIMER_EXPIRED
    #           then PUSH_EVENT   HOLDDOWN_EXPIRED
    # on NeighborOffer in               HoldingDown    finishes in  HoldingDown:       action_update_or_remove_offer
    #     if no level offered REMOVE_OFFER else
    #     if level > leaf then UPDATE_OFFER else REMOVE_OFFER
    # on BetterHAL in                   HoldingDown finishes in     HoldingDown: NO_ACTION
    # on WithdrawNeighborOffer in       HoldingDown finishes in     HoldingDown:      REMOVE_OFFER
    # on ChangeLocalLeafIndications in  HoldingDown finishes in     ComputeBestOffer: action_store_leaf_flag
    # on ComputationDone in             HoldingDown finishes in     HoldingDown: NO_ACTION

    # on    CHANGE_LOCAL_LEAF_INDICATIONS in  UpdatingClients    finishes in        ComputeBestOffer: STORE_LEAF_FLAGS
    # on    LOST_HAT in                       UpdatingClients    finishes in        ComputeBestOffer: NO_ACTION
    # on    BetterHAT in                      UpdatingClients  finishes in          ComputeBestOffer: NO_ACTION
    # on    ShortTic in                       UPDATING_CLIENTS    finishes in       UPDATING_CLIENTS:
    # on    LostHAL in                        UpdatingClients    finishes in        HOLDING_DOWN: action_update_holddown_timer_on_lost_hal
    #     if any southbound adjacencies present
    #         then update holddown timer to normal duration
    #         else fire   holddown    timer    immediately
    # on    NeighborOffer in                   UpdatingClients    finishes in       UpdatingClients: action_update_or_remove_offer
    #     if no level offered REMOVE_OFFER else
    #     if level > leaf then UPDATE_OFFER else REMOVE_OFFER
    # on ChangeLocalConfiguredLevel in          UpdatingClients finishes in         ComputeBestOffer: action_store_level
    # on BetterHAL in                           UpdatingClients finishes in         ComputeBestOffer: NO_ACTION
    # on WithdrawNeighborOffer in               UpdatingClients finishes in         UpdatingClients: REMOVE_OFFER


    # on Entry into UpdatingClients: action_update_all_lie_fsm_with_computation_results
    # on Entry into ComputeBestOffer: LEVEL_COMPUTE

   #  Following words are used for well known procedures:
   # 1.  PUSH Event: pushes an event to be executed by the FSM upon exit  of this action
   # 2.  COMPARE_OFFERS: checks whether based on current offers and held    last results the events BetterHAL/LostHAL/BetterHAT/LostHAT are       necessary and returns them
   # 3.  UPDATE_OFFER: store current offer and COMPARE_OFFERS, PUSH   according events
   # 4.  LEVEL_COMPUTE: compute best offered or configured level and HAL/  HAT, if anything changed PUSH ComputationDone
   # 5.  REMOVE_OFFER: remove the according offer and COMPARE_OFFERS, PUSH       according events
   # 6.  PURGE_OFFERS: REMOVE_OFFER for all held offers, COMPARE OFFERS,       PUSH according events

    #4.2.9.4.Level Determination Procedure

    # A node starting up with UNDEFINED_VALUE (i.e. without a
    # CONFIGURED_LEVEL or any leaf or superspine flag) MUST follow those
    # additional procedures:

    # 1.  It advertises its LEVEL_VALUE on all LIEs (observe that this can
    # be UNDEFINED_LEVEL which in terms of the schema is simply an
    # omitted optional value).

    # 2.  It chooses on an ongoing basis from all VOLs the value of
    # MAX(HAL-1,0) as its DERIVED_LEVEL.  The node then starts to
    # advertise this derived level.

    # 3.  A node that lost all adjacencies with HAL value MUST hold down
    # computation of new DERIVED_LEVEL for a short period of time
    # unless it has no VOLs from southbound adjacencies.  After the
    # holddown expired, it MUST discard all received offers, recompute
    # DERIVED_LEVEL and announce it to all neighbors.

    # 4.  A node MUST reset any adjacency that has changed the level it is
    # offering and is in three way state.

    # 5.  A node that changed its defined level value MUST readvertise its
    # own TIEs (since the new `PacketHeader` will contain a different
    # level than before).  Sequence number of each TIE MUST be
    # increased.

    # 6.  After a level has been derived the node MUST set the
    # `not_a_ztp_offer` on LIEs towards all systems extending a VOL for
    # HAL.

    # A node starting with LEVEL_VALUE being 0 (i.e. it assumes a leaf
    # function by being configured with the appropriate flags or has a
    # CONFIGURED_LEVEL of 0) MUST follow those additional procedures:

    # 1.  It computes HAT per procedures above but does NOT use it to
    # compute DERIVED_LEVEL.  HAT is used to limit adjacency formation
    # per Section 4.2.2.

    # on LostHAT in ComputeBestOffer finishes in ComputeBestOffer:
    #       LEVEL_COMPUTE

    def i_am_a_leaf(self):
        return False

    def remove_offer(self, offer):
        for level in -al.keys():
            if offer.systemId in _al[level]:
                del _al[level][offer.systemId]

    #
    def update_offer(self, offer):
        if not offer.level in self.al:
            self.al[offer.level] = {}

        self.al[offer.level][offer.systemId] = offer
        pass



    def compare_offers(self):



    def action_no_action(self):
        pass

    def action_level_compute(self):
        # TODO:
        if not i_am_a_leaf(self):
            highest_level = max(al.keys())



            if len(al[highest_level]) >=  ZTP_MIN_NUMBER_OF_PEER_FOR_LEVEL


        highest_level = common.constants.leaf_level
        for level in al.keys():
            if len(al[level]) >=  ZTP_MIN_NUMBER_OF_PEER_FOR_LEVEL
                if level >= highest_level
                    highest_level = level

        if highest_level != common.constants.leaf_level
            return highest_level

        return max(al.keys())


    #on ChangeLocalLeafIndications in UpdatingClients finishes in ComputeBestOffer: store leaf flags
    def action_store_leaf_flag(self):
        # TODO:
        pass



    def action_update_or_remove_offer(self, offer):

        # TODO:
        #          if no level offered REMOVE_OFFER else
        #          if level > leaf then UPDATE_OFFER else REMOVE_OFFER

        if offer is not None and offer.is_a_ztp_offer
        current_hal = self.hal
        self.hal = self.compute_best_offer()
        # TODO: trigger something if it changed

    #
    def action_store_level(self):
        # TODO:
        pass

    #

      #
    def action_purge_offers(self):
        # TODO:
        pass
    #

    def action_remove_offer(self):
        # TODO:
        pass
    #
    def action_check_hold_time_expired(self):
        # on LostHAL in ComputeBestOffer finishes in HoldingDown: if any
        # southbound adjacencies present update holddown timer to normal
        # duration else fire holddown timer immediately
        self.info(self._log, "_time_ticks_since_lie_received = {}")
        if self._time_ticks_since_lie_received == None:
            return False
        self._time_ticks_since_lie_received += 1
        if self._time_ticks_since_lie_received >= self.holdtime:
            self._fsm.push_event(self.Event.HOLD_DOWN_EXPIRED)



    def action_update_all_lie_fsm_with_computation_results(self):
        # TODO:
        pass
    #

    def action_update_holddown_timer_on_lost_hal(self):

        #     if any southbound adjacencies present
        #         then update holddown timer to normal duration
        #         else fire   holddown    timer    immediately

        # TODO:
        pass

        #


    state_updating_clients_transitions = {
        Event.CHANGE_LOCAL_LEAF_INDICATIONS:    (State.COMPUTE_BEST_OFFER, [action_store_leaf_flag]),
        Event.LOST_HAT:                         (State.COMPUTE_BEST_OFFER, [action_no_action]),
        Event.BETTER_HAT:                       (State.COMPUTE_BEST_OFFER, [action_no_action]),
        Event.SHORT_TICK_TIMER:                 (None, [action_no_action]),
        Event.LOST_HAL:                         (State.HOLDING_DOWN, [action_update_holddown_timer_on_lost_hal]),
        Event.NEIGHBOR_OFFER:                   (None, [action_update_or_remove_offer]),
        Event.CHANGE_LOCAL_CONFIGURED_LEVEL:    (State.COMPUTE_BEST_OFFER, [action_store_level]),
        Event.BETTER_HAL:                       (State.COMPUTE_BEST_OFFER, [action_no_action]),
        Event.WITH_DRAW_NEIGHBOROFFER:          (None, [action_remove_offer]),

    }

    state_holding_down_transitions = {
        Event.LOST_HAT:                         (None, [action_no_action]),
        Event.LOST_HAL:                         (None, [action_no_action]),
        Event.BETTER_HAT:                       (None, [action_no_action]),
        Event.CHANGE_LOCAL_CONFIGURED_LEVEL:    (State.COMPUTE_BEST_OFFER,[action_store_level]),
        Event.HOLDDOWN_EXPIRED:                 (State.COMPUTE_BEST_OFFER,[action_purge_offers]),
        Event.SHORT_TICK_TIMER:                 (None, [action_check_hold_time_expired]),
        Event.NEIGHBOR_OFFER:                   (None, [action_update_or_remove_offer]),
        Event.BETTER_HAL:                       (None, [action_no_action]),
        Event.WITH_DRAW_NEIGHBOROFFER:          (None, [action_remove_offer]),
        Event.CHANGE_LOCAL_LEAF_INDICATIONS:    (State.COMPUTE_BEST_OFFER, [action_store_leaf_flag]),
        Event.COMPUTATION_DONE:                 (None, [action_no_action])


    }

    state_compute_best_offer_transitions = {
        Event.LOST_HAT:                         (None, [action_level_compute]),
        Event.NEIGHBOR_OFFER:                   (None, [action_update_or_remove_offer]),
        Event.BETTER_HAL:                       (None, [action_level_compute]),
        Event.SHORT_TICK_TIMER:                 (None, [action_no_action]),
        Event.COMPUTATION_DONE:                 (State.UPDATING_CLIENTS, [action_no_action]),
        Event.CHANGE_LOCAL_CONFIGURED_LEVEL:    (None, [action_store_level, action_level_compute]),
        Event.LOST_HAL:                         (State.HOLDING_DOWN, [action_update_holddown_timer_on_lost_hal]),
        Event.BETTER_HAT:                       (None, [action_level_compute]),
        Event.WITH_DRAW_NEIGHBOROFFER:          (None, [action_remove_offer]),
        Event.CHANGE_LOCAL_LEAF_INDICATIONS:    (None, [action_store_leaf_flag, action_level_compute])



    }

    transitions = {
        State.UPDATING_CLIENTS: state_updating_clients_transitions,
        State.HOLDING_DOWN: state_holding_down_transitions,
        State.COMPUTE_BEST_OFFER: state_compute_best_offer_transitions
    }

    state_entry_actions = {
        State.UPDATING_CLIENTS:     [action_update_all_lie_fsm_with_computation_results],
        State.COMPUTE_BEST_OFFER:   [action_level_compute]
    }


    def info(self, logger, msg):
        logger.info("[{}] {}".format(self._log_id, msg))

    def warning(self, logger, msg):
        logger.warning("[{}] {}".format(self._log_id, msg))


    def __init__(self, node, config):

        self._node = node
        self._name = 'ztp'
        self.al={0:{}}
        self.hal = common.constants.leaf_level
        # TODO: Make the default metric/bandwidth depend on the speed of the interface
        self._log = node._log.getChild("ztp")
        self.info(self._log, "Zero touch provisioning state machine")
        self._log_id = node._log_id + "-{}".format(self._name)
        self._fsm_log = self._log.getChild("fsm")
        #TODO take ztp hold time from init file
        self._holdtime = 1
        self._fsm = fsm.FiniteStateMachine(
            state_enum = self.State,
            event_enum = self.Event,
            transitions = self.transitions,
            state_entry_actions = self.state_entry_actions,
            initial_state = self.State.COMPUTE_BEST_OFFER,
            action_handler = self,
            log = self._fsm_log,
            log_id = self._log_id)
        self._one_second_timer = timer.Timer(1.0, lambda: self._fsm.push_event(self.Event.SHORT_TICK_TIMER))


