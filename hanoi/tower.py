class Tower:
    def __init__(self):
        self.disc_sizes: list[int] = []
    
    def push(self, disc_size: int) -> None:
        if len(self.disc_sizes) > 0 and disc_size > self.disc_sizes[-1]:
            raise ValueError('Die Scheibe ist zu groß!')
            
        self.disc_sizes.append(disc_size)

    def pop(self) -> int:
        if len(self.disc_sizes) == 0:
            raise ValueError('Der Turm ist leer!')
        
        return self.disc_sizes.pop()

    def peek(self) -> int:
        if len(self.disc_sizes) == 0:
            raise ValueError('Der Turm ist leer!')
        
        return self.disc_sizes[-1]
