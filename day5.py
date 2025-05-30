class Pet:
    def __init__(self, name, species, age):
        self.name= name
        self.species = species
        self.age = age
    
    def make_sound(self):
        print(f"Am a {self.name},This")

    def eat(self):
        print("i eat food ") 

cat = Pet("dog","canivore", 14)
cat.make_sound()
cat.eat()

class Lion(Pet):
    def __init__(self, name, species, age,sound):
        super().__init__(name, species, age)
        self.sound =sound
    
    def make_sound(self):
        print(f"a {self.name}'s sound is {self.sound} ")

x= Lion("lion", "canivore", 25, "roars")
x.make_sound()
x.eat()
        
        
        


