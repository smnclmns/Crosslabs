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

//Generated stub

Blockly.JavaScript['spritzpumpe'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};