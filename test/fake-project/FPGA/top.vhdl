library IEEE;
use IEEE.std_logic_1164.all;

entity top is
   port (
      data_i :  in std_logic;
      data_o : out std_logic
   );
end entity top;

architecture RTL of top is
begin

   inst: entity work.core
      port map (
         data_i => data_i,
         data_o => data_o
      );

end architecture RTL;
