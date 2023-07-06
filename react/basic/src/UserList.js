import React, { useEffect } from 'react';

const User = React.memo(function User({ user, onRemove, onToggle }) {
    useEffect(() => {
        console.log(user)
    });

    return (
        <div>
            <b style={{ corsor: 'pointer', color: user.active ? 'green' : 'black' }} onClick={() => onToggle(user.id)}>{user.username}</b>
            <span>({user.email})</span>
            <button onClick={() => onRemove(user.id)}> 삭제</button>
        </div >
    )
});

function UserList({ users, onRemove, onToggle }) {
    return (
        <div>
            {users.map(user => (
                <User user={user} key={user.id} onRemove={onRemove} onToggle={onToggle} />
            ))}
        </div>
    );
}

export default React.memo(UserList);