const msgSuccess = (commit, msg = "Thank you!!") => {
    return commit(
        "notificationModule/setToastMsg",
        {
            msg: msg,
            type: "success"
        },
        { root: true }
    );
};

const msgError = (commit, msg = "Opps, try again later") => {
    return commit(
        "notificationModule/setToastMsg",
        {
            msg: msg,
            type: "error"
        },
        { root: true }
    );
};

export { msgError, msgSuccess };
