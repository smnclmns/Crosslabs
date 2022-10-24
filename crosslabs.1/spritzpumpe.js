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
