const socketio = require('socket.io')
const http = require('http')

const express=require('express')
const app=express()

app.use(express.json())

const server=http.createServer(app)
const io = socketio(server)

var client = undefined

io.on('connection', (socket) => {
    console.log('conntion established')
    client = socket.id
})

// app.get('/lol', (req, res) => {
//     console.log(client)
//     io.to(client).emit('newData',req.query.newData) //req.body
//     res.send()
// })

app.post('/lol', (req, res) => {
    console.log(client)
    io.to(client).emit('newData',req.body)
    res.send()
})


server.listen(3000,()=>{
    console.log('running')
})



