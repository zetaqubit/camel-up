from dataclasses import dataclass

@dataclass
class CamelMove:
  camel: int  # range [1, n_camels]
  spaces: int  # range [1, n_max_roll]
