grammar Choreography;

choreography: command+;

command: moveCommand | syncCommand | repeatCommand | setFrpsCommand | waitCommand;

moveCommand: 'move' '(' ('all' | motor) ',' degree (',' speed)? ')';
syncCommand: 'sync' '{' moveCommand+ '}';
repeatCommand: 'repeat' times '{' command+ '}';
setFrpsCommand: 'set_frps' speed;
waitCommand: 'wait' '(' seconds ')';

motor: INTEGER;
degree: DECIMAL | INTEGER;
speed: DECIMAL | INTEGER;
seconds: DECIMAL | INTEGER;
times: INTEGER ;


INTEGER: [0-9]+;
DECIMAL: [0-9]+('.'[0-9]+)?;

COMMENT: '#' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;     // Whitespace
