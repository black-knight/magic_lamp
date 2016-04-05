var MAZE = MAZE || {};

MAZE.Play = new Kiwi.State( "Play" );

var maxPlayers = 4;

var borderLayer = null;
var tileLayers = [];

/**
* The PlayState in the core state that is used in the game.
*
* It is the state where majority of the functionality occurs 'in-game' occurs.
*/

MAZE.Play.preload = function () {
    this.addJSON( 'tilemap', 'assets/maps/sample.json' );
    this.addSpriteSheet( 'tiles', 'assets/img/tiles/board_tiles.png', 40, 40 );
}

/**
* This create method is executed when a Kiwi state has finished loading
* any resources that were required to load.
*/
MAZE.Play.create = function () {

	Kiwi.State.prototype.create.call( this );

    this.tilemap = new Kiwi.GameObjects.Tilemap.TileMap( this, 'tilemap', this.textures.tiles );

    borderLayer = this.tilemap.getLayerByName( "Border Layer" );
    this.addChild( borderLayer );

    tileLayers.push( this.tilemap.getLayerByName("Tile Layer 1" ));
    this.addChild( tileLayers[0] );

    tileLayers.push( this.tilemap.getLayerByName("Tile Layer 2" ));
    this.addChild( tileLayers[1] );

    borderLayer.alpha = 1.0;

    statusTextField = new Kiwi.HUD.Widget.TextField(this.game, '', 100, 10);
    this.game.huds.defaultHUD.addWidget(statusTextField);

    statusTextField.style.color = '#00ff00';
    statusTextField.style.fontSize = '14px';
    statusTextField.style.textShadow = '-1px -1px 5px black, 1px -1px 5px black, -1px 1px 5px black, 1px 1px 5px black';

    maze = new MazeInfo()
    maze.client.debug_textField = statusTextField
    maze.startup()
};


MAZE.Play.update = function() {

	Kiwi.State.prototype.update.call( this );
};
