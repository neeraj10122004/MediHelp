const mongoose = require('mongoose');
const findOrCreate = require('mongoose-findorcreate');

const userSchema = new mongoose.Schema({
    googleId: { type: String, unique: true },
    email: { type: String, unique: true },
    name: String,
    query: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Query' }],
    photourl: String
});

userSchema.plugin(findOrCreate);

module.exports = mongoose.model('User', userSchema);