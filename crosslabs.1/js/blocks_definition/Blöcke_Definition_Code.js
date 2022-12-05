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
Blockly.Blocks['arduinobib'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldLabelSerializable("Bibliotheken"), "Text")
        .appendField(new Blockly.FieldDropdown([["Adafruit","op1"], ["Stepper","op2"], ["Wire","op3"], ["FakeLib","op4"], ["FakeLib2","op5"]]), "DD1")
        .appendField(new Blockly.FieldDropdown([["Adafruit","op1"], ["Stepper","op2"], ["Wire","op3"], ["FakeLib","op4"], ["FakeLib2","op5"]]), "DD2")
        .appendField(new Blockly.FieldDropdown([["Adafruit","op1"], ["Stepper","op2"], ["Wire","op3"], ["FakeLib","op4"], ["FakeLib2","op5"]]), "DD3");
    this.setColour(225);
 this.setTooltip("");
 this.setHelpUrl("");
  }
}
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

Blockly.JavaScript['arduinobib'] = function(block) {
  var dropdown_dd1 = block.getFieldValue('DD1');
  var dropdown_dd2 = block.getFieldValue('DD2');
  var dropdown_dd3 = block.getFieldValue('DD3');

  if (dropdown_dd1 == "op4" || dropdown_dd3 == "op4" || dropdown_dd2 == "op4" || dropdown_dd1 == "op5" || dropdown_dd2 == "op5" || dropdown_dd3 =="op5") {
    var code = "alert('wrong')";
  }
  else if (dropdown_dd1 == dropdown_dd2 && dropdown_dd2== dropdown_dd3){
    var code ="alert('wrong')";
  }
  else if (dropdown_dd1 == dropdown_dd3 || dropdown_dd2== dropdown_dd3 || dropdown_dd2==dropdown_dd1){
    var code ="alert('wrong')";
  }
  else {
  var code = "alert('right')";
}

  return code;
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
