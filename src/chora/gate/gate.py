class ChoraGate:

    def evaluate(self, confidence):
        if confidence > 0.8:
            return "ALLOW"
        elif confidence > 0.5:
            return "ESCALATE"
        else:
            return "HALT"
