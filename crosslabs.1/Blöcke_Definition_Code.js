Blockly.Blocks['spritzpumpe'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Spritzpumpe");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
 this.setTooltip("Pumpen befehl");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['lichtsensor'] = {
  init: function() {
    this.appendValueInput("Lichtwert")
        .setCheck("Number")
        .appendField("Lichtsensor");
    this.setPreviousStatement(true, null);
    this.setColour(330);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['geschwindigkeit'] = {
  init: function() {
    this.appendValueInput("Geschwindigkeit")
        .setCheck("")
        .appendField(new Blockly.FieldDropdown([["Langsam","Langsam"], ["Schnell","Schnell"], ["Normal","Normal"]]), "NAME")
        .appendField("Geschwindigkeit");
    this.setOutput(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['library'] = {
  init: function() {
    this.appendValueInput("Library1")
        .setCheck("String")
        .appendField("Library include");
    this.appendValueInput("Library2")
        .setCheck("String");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['adafruit'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Adafruit_AS726x.h");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(225);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['stepper'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Speedystepper");
    this.setOutput(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['wire'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Wire.h");
    this.setOutput(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['fake_lib_1'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Fake LIB");
    this.setOutput(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['fake_lib_2'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("FAKE LIB2");
    this.setOutput(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['arduino_outputs'] = {
  init: function() {
    this.appendValueInput("LED")
        .setCheck("Number")
        .appendField("LED Pin");
    this.appendValueInput("Step")
        .setCheck("Number")
        .appendField("Motor Step Pin");
    this.appendValueInput("DIrection")
        .setCheck("Number")
        .appendField("Motor Direction Pin");
    this.setColour(300);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['titrationsphasen'] = {
  init: function() {
    this.appendStatementInput("Titrationsphasen")
        .setCheck("Boolean")
        .appendField("Titrationsphasen")
        .appendField(new Blockly.FieldDropdown([["Phase1","1"], ["Phase2","2"], ["endphase","end"], ["Fertig","fertig"]]), "Titrationsphasen");
    this.setColour(230);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
//Generated stub

Blockly.JavaScript['spritzpumpe'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
Blockly.JavaScript['lichtsensor'] = function(block) {
  var value_lichtwert = Blockly.JavaScript.valueToCode(block, 'Lichtwert', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['geschwindigkeit'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  var value_geschwindigkeit = Blockly.JavaScript.valueToCode(block, 'Geschwindigkeit', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};
Blockly.JavaScript['library'] = function(block) {
  var value_library1 = Blockly.JavaScript.valueToCode(block, 'Library1', Blockly.JavaScript.ORDER_ATOMIC);
  var value_library2 = Blockly.JavaScript.valueToCode(block, 'Library2', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['adafruit'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['stepper'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['wire'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['fake_lib_1'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['fake_lib_2'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['arduino_outputs'] = function(block) {
  var value_led = Blockly.JavaScript.valueToCode(block, 'LED', Blockly.JavaScript.ORDER_ATOMIC);
  var value_step = Blockly.JavaScript.valueToCode(block, 'Step', Blockly.JavaScript.ORDER_ATOMIC);
  var value_direction = Blockly.JavaScript.valueToCode(block, 'DIrection', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};

Blockly.JavaScript['titrationsphasen'] = function(block) {
  var dropdown_titrationsphasen = block.getFieldValue('Titrationsphasen');
  var statements_titrationsphasen = Blockly.JavaScript.statementToCode(block, 'Titrationsphasen');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};
