import json

class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file
        #print("Hi, I'm an automaton!")

    def validate(self):
        """Return a Boolean

        Returns True if the config file is valid,
        and raises a ValidationException if the config is invalid.
        """
        Scount = 0
        with open(self.config_file) as f:
            at = self.read_input(f.read())
        
        # print(json.dumps(at, indent = 4))

        for state in at['states'].keys():
            if 'S' in at['states'][state]:
                Scount += 1
                at['start'] = state

        self.data = at
        if Scount != 1:
            raise Exception('ValidationException: Mai multe stagii de tip \'S\'')

        for transition in at['transitions'].keys():
            if not transition in at['states'].keys():
                raise Exception('ValidationException: State ' + transition + ' declaration missing!')
            for line in at['transitions'][transition].keys():
                if not line in at['sigma']:
                    raise Exception('ValidationException: Sigma ' + line + ' declaration missing!')
                for q in at['transitions'][transition][line]:
                    if not q in at['states'].keys():
                        raise Exception('ValidationException: State ' + at['transitions'][transition][line] + ' declaration missing!')

        return "Everything worked out."

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass

    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        sigma = []
        states = {}
        transitions = {}
        foundsigma = False
        foundstates = False
        foundtransitions = False
        lines = input_str.split("\n")
        i = 0
        while True:
            i += 1
            if i >= len(lines):
                break
            line = lines[i].strip()
            if not len(line) or line[0] == '#':
                continue # linia este goala sau comentariu

            else:
                if line[-1] == ':':
                    section = line[:-1].strip()
                    if section.lower() == 'sigma':
                        foundsigma = True
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            line = lines[i].strip()
                            if line == 'End':
                                break
                            else:
                                sigma.append(line)

                    elif section.lower() == 'states':
                        foundstates = True
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            line = lines[i].strip()
                            if line == 'End':
                                break
                            else:
                                content = [i.strip() for i in line.split(',')]
                                if len(content) >= 3:
                                    raise Exception('RejectionException la linia ' + str(i) + '. Pe fiecare linie trebuie sa se afle maxim 2 elemente separate cu virgula!')
                                else:
                                    if len(content) == 1:
                                        if content[0][-1] in 'FS':
                                            raise Warning('NameWarning: State cu nume care se termina in S sau F la linia ' + str(i))
                                        states[content[0]] = ''
                                    else:
                                        states[content[0]] = content[1]

                    elif section.lower() == 'transitions':
                        foundtransitions = True
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            line = lines[i].strip()
                            if line == 'End':
                                break
                            else:
                                content = [i.strip() for i in line.split(',')]
                                if len(content) != 3:
                                    raise Exception('RejectionException la linia ' + str(i) + '. Pe fiecare linie trebuie sa se afle 3 elemente separate cu virgula!')
                                
                                else:
                                    if not content[0] in transitions:
                                        transitions[content[0]] = {content[1] : [content[2]]}
                                    else:
                                        if content[1] in transitions[content[0]].keys():
                                            transitions[content[0]][content[1]].append(content[2])
                                        else:
                                            transitions[content[0]][content[1]] = [content[2]]



                else:
                    raise Exception('RejectionException la linia ' + str(i) + '. Linia nu se termina in \' :\'')
        if not foundsigma:
            raise Exception('RejectionException: Lipseste Sigma')
        if not foundstates:
            raise Exception('RejectionException: Lipseste States')
        if not foundtransitions:
            raise Exception('RejectionException: Lipseste Transitions')
        
        for q in states:
            if not q in transitions.keys():
                transitions[q] = {}
        # print  ({'states' : states, 'sigma' : sigma, 'transitions' : transitions})
        return {'states' : states, 'sigma' : sigma, 'transitions' : transitions}
    

if __name__ == "__main__":
    a = Automaton('config.txt')
    print(a.validate())
    print(a.data)
    