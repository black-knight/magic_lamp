MAZE = MAZE or {}
MAZE.Game = new Kiwi.State("Game")

tileLayers = []

mazeGame = null

MAZE.Game.preload = ->
    @addJSON("tilemap", "assets/maps/maze.json")
    @addSpriteSheet("tiles", "assets/img/tiles/board_tiles.png", 40, 40)
    @addImage("logo", "assets/img/menu/title.png")

MAZE.Game.create = ->
    Kiwi.State::create.call(this)

    mazeGame = new MazeGame(this)
    mazeGame.start()

MAZE.Game.shutDown = ->
    Kiwi.State::shutDown.call(this)
    mazeGame.stop()

MAZE.Game.update = ->
    Kiwi.State::update.call(this)



class MazeGame

    constructor: (@kiwiState) ->
        @client = new Client()
        @mazeModel = new MazeModel()

    start: ->
        @setupUi()
        @client.connect((() => @reset()), ((json) => @onMessage(json)))

    stop: ->
        @client.disconnect()

    reset: ->
        @client.reset()

    onMessage: (json) ->
        switch json["action"]
            when "reset" then @initializeBoard()
            when "initializeTiledBoard" then @ready()



    setupUi: ->

        # Setup logo
        @logo = new Kiwi.GameObjects.StaticImage(@kiwiState, @kiwiState.textures.logo, 0, 0)
        @logo.alpha = 0.0

        # Setup tilemap
        @tilemap = new Kiwi.GameObjects.Tilemap.TileMap(@kiwiState, "tilemap", @kiwiState.textures.tiles)
        borderLayer = @tilemap.getLayerByName("Border Layer")

        @tileLayers = []
        @tileLayers.push(@tilemap.getLayerByName("Tile Layer 1"))
        @tileLayers.push(@tilemap.getLayerByName("Tile Layer 2"))

        @tileLayers[0].alpha = 1.0
        @tileLayers[1].alpha = 0.0

        @visibleLayer = 0

        # Add elements to UI
        @kiwiState.addChild(borderLayer)
        @kiwiState.addChild(@tileLayers[0])
        @kiwiState.addChild(@tileLayers[1])
        @kiwiState.addChild(@logo)

        # Setup debug log
        statusTextField = new Kiwi.HUD.Widget.TextField(@kiwiState.game, "", 100, 10)
        statusTextField.style.color = "#00ff00"
        statusTextField.style.fontSize = "14px"
        statusTextField.style.textShadow = "-1px -1px 5px black, 1px -1px 5px black, -1px 1px 5px black, 1px 1px 5px black"
        @client.debug_textField = statusTextField
        @kiwiState.game.huds.defaultHUD.addWidget(statusTextField)

        # Fade logo
        setTimeout(() =>
            fadeLogoTween = @kiwiState.game.tweens.create(@logo);
            fadeLogoTween.to({ alpha: 1.0 }, 2000, Kiwi.Animations.Tweens.Easing.Linear.In, true)
        , 500)



    initializeBoard: ->
        @client.initializeTiledBoard(@mazeModel.width, @mazeModel.height)

    waitForStartPositions: ->
        @client.reportBackWhenTileAtAnyOfPositions([[10, 10], [11, 10], [12, 10]])

    ready: ->
        # Fade maze
        setTimeout(() =>
            @mazeModel.createRandomMaze()
            @updateMaze()
        , 1500)

        # Wait for start positions
        setTimeout(() =>
            @waitForStartPositions()
        , 2500)



    updateMaze: ->
        @visibleLayer = if @visibleLayer == 0 then 1 else 0

        for y in [0..@mazeModel.height - 1]
            for x in [0..@mazeModel.width - 1]
                entry = @mazeModel.entryAtCoordinate(x, y)
                @tileLayers[@visibleLayer].setTile(x, y, entry.tileIndex)

        alpha = if @visibleLayer == 0 then 0.0 else 1.0

        fadeMazeTween = @kiwiState.game.tweens.create(@tileLayers[1]);
        fadeMazeTween.to({ alpha: alpha }, 1000, Kiwi.Animations.Tweens.Easing.Linear.In, true)
