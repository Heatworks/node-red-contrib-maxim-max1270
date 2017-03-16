var PythonShell = require('python-shell');

module.exports = function(RED) {
    function MaximMax1270Node(config) {
        RED.nodes.createNode(this,config);
        var node = this;

        var scriptPath = './spi_read.py'
        
        var args = []
        args = [parseInt(config.sampling),parseInt(config.reporting), parseInt(config.channel)]

        var pyshell = new PythonShell(scriptPath, { scriptPath: __dirname, args: args });

        pyshell.on('message', function (message) {
            node.send({
                payload: message
            });
        });

        this.on("close", function() {
            if (pyshell) {
                pyshell.end(); 
            }
        });
    }
    RED.nodes.registerType("maxim-max31855", MaximMax1270Node);
}