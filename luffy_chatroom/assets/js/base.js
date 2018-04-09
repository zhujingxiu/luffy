/**
 * Created by admin on 2018/4/8.
 */
Date.prototype.formattor = function (format) {
    var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1
                ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
        }
    }
    return format;
};

var luffy = {

    init_user: function () {
        var _users = sessionStorage.getItem('user');
        if (!_users) {
            $.get('assets/data/user.json', {_r: Math.random()}, function (json) {
                var _username = {}, _users = {};
                for (var i in json) {
                    _user = json[i];
                    _username[_user.username] = _user.uid;
                    _users[_user.uid] = _user;
                }
                sessionStorage.setItem('user', JSON.stringify(_users));
                sessionStorage.setItem('username', JSON.stringify(_username));
            }, 'json')
        }
    },
    init_menu: function (el) {
        var _this = this;
        var menu = new BootstrapMenu('.node-'+el, {
            fetchElementData: function ($rowElem) {
                return $('#' + el).treeview('getNode', $rowElem.data('nodeid'));
            },
            actionsGroups: [
                ['editName'],
                ['addFriend','delFriend'],
                ['viewDetail']
            ],
            actions: {
                editName: {
                    name: '修改备注',
                    iconClass: 'glyphicon glyphicon-edit',
                    onClick: function (row) {
                        toastr.warning('此功能暂未开放，后期添加');
                    }
                },
                addFriend: {
                    name: '添加好友',
                    iconClass: 'glyphicon glyphicon-plus-sign',
                    onClick: function (row) {
                        console.log("'Set editable' clicked on '" + row.text + "'");
                        $('#friendModal .friend-info-avatar > img').attr('src','assets/images/avatar/'+row.avatar).next('p').html(row.text).next('input[name="friend_id"]').val(row.uid);
                        $('#friendModal').modal('show')
                    },
                    isEnabled: function (row) {
                        return _this.has_friend(row.uid)==-1;
                    },
                    isShown: function(row) {
                        return el=='treeGroup';
                    }
                },
                delFriend: {
                    name: '删除好友',
                    iconClass: 'glyphicon glyphicon-plus-sign',
                    onClick: function (row) {
                        toastr.warning('此功能暂未开放，后期添加');
                    },
                    isShown: function(row) {
                        return el=='treeFriend';
                    }
                },
                viewDetail: {
                    name: '查看详情',
                    iconClass: 'glyphicon glyphicon-list-alt',
                    onClick: function (row) {
                        toastr.warning('此功能暂未开放，后期添加');
                    }
                }
            }
        });
        return menu;
    },
    has_friend:function (uid) {
        var member = this.check_logged();
        if (!member) {
            return false;
        }
        var _friends = sessionStorage.getItem('friend-ids-' + member.uid);
        if(!_friends){
            return false;
        }
        return $.inArray(uid,JSON.parse(_friends));
    },
    check_logged: function () {
        var _member = sessionStorage.getItem('member');
        if (!_member) {
            return false
        }
        return JSON.parse(_member)
    },
    edit_password:function () {
        toastr.warning('此功能暂未开放，后期添加');
    },
    render_group: function () {
        var group = sessionStorage.getItem('group');
        if (!group) {
            $.get('assets/data/group.json', {_r: Math.random()}, function (json) {
                group = JSON.stringify(json);
                sessionStorage.setItem('group', group);
            })
        }
        return JSON.parse(group);
    },
    render_friend: function () {
        var member = this.check_logged();
        if (!member.uid) {
            toastr.warning('请先登录');
            return false
        }
        var friends = sessionStorage.getItem('friend-' + member.uid);
        if (!friends) {
            $.get('assets/data/friend.json', {_r: Math.random()}, function (json) {
                var _friends = [];
                for(var i in json){
                    var _friend = json[i];
                    _friends.push(_friend.uid)
                }
                friends = JSON.stringify(_friends);
                sessionStorage.setItem('friend-' + member.uid, JSON.stringify(json));
                sessionStorage.setItem('friend-ids-' + member.uid, friends);
            },'json')
        }
        return JSON.parse(friends);
    },
    add_friend:function (uid,remark) {
        var member = this.check_logged();
        if (!member.uid) {
            return false
        }
        var _friend = this.get_user(uid);
        var _friend_ids = [];
        var _friends = sessionStorage.getItem('friend-' + member.uid);
        if(!_friends){
            _friends = {};
        }else{
            _friends = JSON.parse(_friends);
            _friend_ids = JSON.parse(sessionStorage.getItem('friend-ids-' + member.uid))
        }
        _friends.push({
            uid: _friend.uid,
            text: _friend.nickname,
            avatar: _friend.avatar,
            icon: "glyphicon glyphicon-user"
        });
        _friend_ids.push(_friend.uid);
        sessionStorage.setItem('friend-' + member.uid,JSON.stringify(_friends));
        sessionStorage.setItem('friend-ids-' + member.uid,JSON.stringify(_friend_ids));
        toastr.success('您已添加好友'+_friend.nickname);
        setTimeout(function () {
            location.reload()
        },2000);

    },
    get_user: function (_user_id) {
        var _users = sessionStorage.getItem('user');
        if (!_users) {
            return false;
        }
        _users = JSON.parse(_users);
        var _user = _users[_user_id];
        if (!_user) {
            return false;
        }
        return _user;
    },
    get_user_by_username: function (username) {
        var _username = sessionStorage.getItem('username');
        if (!_username) {
            return false;
        }
        _username = JSON.parse(_username);
        var _user = _username[username];
        if (!_user) {
            return false
        }
        return this.get_user(_user);
    },
    render_textarea: function (el) {
        $('#' + el).summernote({
            lang: 'zh-CN',
            focus: true,
            minHeight: 100,
            toolbar: [
                ['style', ['bold', 'italic', 'underline']],
                ['fontsize', ['fontsize']],
                ['color', ['color']],
                ['insert', ['link', 'picture', 'emojiList']]
            ],
            hint: {
                match: /:([\-+\w]+)$/,
                search: function (keyword, callback) {
                    callback($.grep(emojis, function (item) {
                        return item.indexOf(keyword) === 0;
                    }));
                },
                template: function (item) {
                    var content = emojiUrls[item];
                    return '<img src="' + content + '" width="20" /> :' + item + ':';
                },
                content: function (item) {
                    var url = emojiUrls[item];
                    if (url) {
                        return $('<img />').attr('src', url).css('width', 20)[0];
                    }
                    return '';
                }
            }
        })
    },
    render_logs: function (uid, member_id) {
        var _log_data = sessionStorage.getItem('chats-' + uid + '-' + member_id);
        if (!_log_data) {
            return '';
        }
        var member = this.check_logged();
        var _logs = JSON.parse(_log_data);
        var _html = '';
        for (var i in _logs) {
            var _is_mine = false;
            var _log = _logs[i];
            var logger = {};
            if (member && _log.uid == member.uid) {
                logger = member;
                _is_mine = true;
            } else {
                logger = this.get_user(_log.uid);
            }
            _html += '<li ' + (_is_mine ? 'class="chat-mine"' : '') + '>';
            _html += '      <div class="chat-user">';
            _html += '          <img src="assets/images/avatar/' + logger.avatar + '" alt="">';
            _html += '          <cite>';
            if (_is_mine) {
                _html += '<i>' + _log.log_time + '</i>' + logger.nickname;
            } else {
                _html += logger.nickname + '<i>' + _log.log_time + '</i>';
            }
            _html += '          </cite>';
            _html += '      </div>';
            _html += '      <div class="chat-text">';
            _html += _log.msg;
            _html += '      </div>';
            _html += '</li>';
        }
        return _html
    },
    send_msg: function (member, uid, _msg, _is_mine) {
        var date = new Date();
        var _now_time = date.formattor('yyyy-MM-dd h:m:s');
        var _html = '<li ' + (_is_mine ? 'class="chat-mine"' : '') + '>';
        _html += '      <div class="chat-user">';
        _html += '          <img src="assets/images/avatar/' + member.avatar + '" alt="">';
        _html += '          <cite>';
        if (_is_mine) {
            _html += '<i>' + _now_time + '</i>' + member.nickname;
        } else {
            _html += member.nickname + '<i>' + _now_time + '</i>';
        }
        _html += '          </cite>';
        _html += '      </div>';
        _html += '      <div class="chat-text">';
        _html += _msg;
        _html += '      </div>';
        _html += '</li>';
        var _log_data = sessionStorage.getItem('chats-' + member.uid + '-' + uid);
        if (_log_data) {
            _log_data = JSON.parse(_log_data);
        } else {
            _log_data = {};
        }
        _log_data[date.getTime()] = {
            'uid': member.uid,
            'log_time': _now_time,
            'msg': _msg
        };
        sessionStorage.setItem('chats-' + member.uid + '-' + uid, JSON.stringify(_log_data));
        sessionStorage.setItem('chats-' + uid + '-' + member.uid, JSON.stringify(_log_data));
        return _html
    },
    login: function (username, password) {
        var info = this.get_user_by_username(username);
        if (!info) {
            return false;
        }
        if (info.password != password) {
            return false;
        }
        sessionStorage.setItem('member', JSON.stringify(info));
        location.reload();
    },
    logout: function () {
        sessionStorage.removeItem('member');
        location.reload()
    },
    auto_reply: function (uid) {
        var member = this.check_logged();
        if (!member) {
            return false;
        }
        var autoReplay = [
            '您好，我现在有事不在，一会再和您联系。<iframe frameborder="0" class="twa twa-smile"></iframe>',
            '你好，我是主人的美女秘书，有什么事就跟我说吧，等他回来我会转告他的。<iframe frameborder="0" class="twa twa-smile"></iframe>',
            '<（@￣︶￣@）>',
            '你要和我说话？你真的要和我说话？你确定自己想说吗？你一定非说不可吗？那你说吧，这是自动回复。<iframe frameborder="0" class="twa twa-kiss"></iframe>',
            ' 你慢慢说，别急……<iframe frameborder="0" class="twa twa-walking"></iframe>'
        ];
        var user = this.get_user(uid);
        return this.send_msg(user, member.uid, autoReplay[Math.floor((Math.random() * autoReplay.length))], false)
    }
};