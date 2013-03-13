(function(){
    DemoBase = function() {
        this.demoContext = $("#demo")[0].getContext('2d');
        this.tileSideLength = 5;
    };

    DemoBase.prototype.draw = function(tilemap){
        for(var col = 0; col < tilemap.length; col++) {
            for(var row = 0; row < tilemap[col].length; row++) {
                this.drawCell(row, col, tilemap[col][row]);
            }
        }
    };

    AutomatonDemo = function() {
        DemoBase.call(this);

        this.states = [
            "rgb(0, 125, 0)", /* Land */
            "rgb(0, 0, 200)", /* Water */
        ];
        $("#title").text("2D Cellular Automaton Demo");
    };

    AutomatonDemo.prototype = new DemoBase();

    AutomatonDemo.prototype.drawCell = function(x, y, state) {
        this.demoContext.fillStyle = this.states[state];
        this.demoContext.fillRect(x * this.tileSideLength,  y * this.tileSideLength, 
                                  this.tileSideLength, this.tileSideLength);
    }; 

    AutomatonDemo.prototype.show = function() {
        var self = this;

        $.ajax({
            url: "/automaton.json",
            cache: false, 
            dataType: "json",
            success: function(data){
                self.draw(data.tilemap);
            }
        });
    };

    PerlinDemo = function() {
        DemoBase.call(this);
        $("#title").text("2D Perlin Noise Demo");
    };

    PerlinDemo.prototype = new DemoBase();

    PerlinDemo.prototype.drawCell = function(x, y, state) {
        this.demoContext.fillStyle = "rgb(" + state + ", " + state + ", " + state + ")"; 
        this.demoContext.fillRect(x * this.tileSideLength,  y * this.tileSideLength, 
                                  this.tileSideLength, this.tileSideLength);
    }; 

    PerlinDemo.prototype.show = function() {
        var self = this;

        $.ajax({
            url: "/perlin.json",
            cache: false,
            dataType: "json",
            success: function(data){
                self.draw(data.tilemap);
            }
        });
    };

    $("#demoSelector").change(function(e){
        var demo;

        switch($(this).val()) {
            case "2dAutomaton":
                demo = new AutomatonDemo();
            break
            case "perlin":
                demo = new PerlinDemo();
            break;
        }
        demo.show();
    });
})();
