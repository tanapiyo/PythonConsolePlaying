- リアルタイムゲームではsetIntervalでメインループを実装
- その中で座標の更新をする
``` javascript
setInterval(tick, 100);
function tick() {
    //座標の更新
    //更新のなかでcanvas描画メソッドを呼ぶ
}
```