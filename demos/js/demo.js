(function(){
    AutomatonDemo = function() {
        this.demoContext = $("#demo")[0].getContext('2d');
        this.states = [
            "rgb(0, 125, 0)", /* Land */
            "rgb(0, 0, 200)", /* Water */
        ];
        this.tileSideLength = 5;
        $("#title").text("2D Cellular Automaton Demo");
    };

    AutomatonDemo.prototype.draw = function(tilemap) {
        for(var col = 0; col < tilemap.length; col++) {
            for(var row = 0; row < tilemap[col].length; row++) {
                this.drawCell(row, col, tilemap[col][row]);
            }
        }
    };

    AutomatonDemo.prototype.drawCell = function(x, y, state) {
        this.demoContext.fillStyle = this.states[state];
        this.demoContext.fillRect(x * this.tileSideLength,  y * this.tileSideLength, 
                                  this.tileSideLength, this.tileSideLength);
    }; 

    AutomatonDemo.prototype.show = function() {
        var self = this;

        $.ajax({
            url: "/automaton.json",
            dataType: "json",
            success: function(data){
                self.draw(data.tilemap);
            }
        });
    }
})();
