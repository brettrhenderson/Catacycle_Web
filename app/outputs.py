import io
import numpy as np
import pandas as pd


def write_cake_sim_data(filename, param_dict, data):
    export_df = pd.DataFrame(pd.concat((data.t_df, data.fit_conc_df, data.fit_rate_df, data.temp_df), axis=1))
    df_inputs = pd.DataFrame([{key: str(value) for (key, value) in param_dict.items()}])

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        export_df.to_excel(writer, sheet_name='FitData', index=False)
        df_inputs.to_excel(writer, sheet_name='InputParams', index=False)


def write_cake_sim_data_temp(param_dict, data):
    tmp_file = io.BytesIO()
    write_cake_sim_data(tmp_file, param_dict, data)

    return tmp_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def write_cake_fit_data(filename, param_dict, data):
    export_df = pd.DataFrame(pd.concat((data.t_df, data.exp_conc_df, data.fit_conc_df, data.fit_rate_df,
                                        data.temp_df), axis=1))
    out_dict = {'Rate Constants': data.k_fit,
                'Rate Constant Errors': data.k_fit_err,
                'Reaction Orders': data.ord_fit,
                'Reaction Order Errors': data.ord_fit_err,
                'Species Poisoning': data.pois_fit,
                'Species Poisoning Errors': data.pois_fit_err,
                'RSS': data.rss,
                'RMSE': data.rmse,
                'MAE': data.mae,
                'R2': data.r2,
                'R2_adj': data.r2_adj,
                'AIC': data.aic,
                'BIC': data.bic}
    df_outputs = pd.DataFrame([{key: str(value) for (key, value) in out_dict.items()}])
    df_inputs = pd.DataFrame([{key: str(value) for (key, value) in param_dict.items()}])

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        export_df.to_excel(writer, sheet_name='FitData', index=False)
        df_outputs.to_excel(writer, sheet_name='OutputParams', index=False)
        df_inputs.to_excel(writer, sheet_name='InputParams', index=False)


def write_cake_fit_data_temp(dict, data):
    tmp_file = io.BytesIO()
    write_cake_fit_data(tmp_file, dict, data)

    return tmp_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


# print CAKE results
def pprint_cake(data):
    print(data.k_fit, data.k_fit_err, data.ord_fit, data.ord_fit_err, data.pois_fit, data.pois_fit_err)
    results = f""
    if isinstance(data.k_fit, (np.ndarray, list, tuple)) and len(data.k_fit) > 0:
        results += f"""Rate Constants (k):
Fitted: {", ".join(f"{i:.4g}" for i in data.k_fit)}
Error: {", ".join(f"{i:.2g}" for i in data.k_fit_err)}
"""
    if isinstance(data.ord_fit, (np.ndarray, list, tuple)) and len(data.ord_fit) > 0:
        results += f"""
Reaction Orders:
Fitted: {", ".join(f"{i:.4g}" for i in data.ord_fit)}
Error: {", ".join(f"{i:.2g}" for i in data.ord_fit_err)}
"""
    if isinstance(data.pois_fit, (np.ndarray, list, tuple)) and len(data.pois_fit) > 0:
        results += f"""
Species Poisoning:
Fitted: {", ".join(f"{i:.4g}" for i in data.pois_fit)}
Error: {", ".join(f"{i:.2g}" for i in data.pois_fit_err)}
"""
    results += f"""
Quality of Fit Metrics:
RMSE: {data.rmse:.4g} | MAE: {data.mae:.4g}"""
    if data.r2:
        results += f"""
R²: {data.r2:.4g} | Adjusted R²: {data.r2_adj:.4g}
AIC: {data.aic:.4g} | BIC: {data.bic:.4g}\n
"""

    results += f"Download file to see full results"

    return results



def write_cc_fit_data(filename, param_dict, gen_data, apply_data):
    # param_dict = {key: np.array([value]) for (key, value) in param_dict.items()}
    param_dict = {key: [str(value)] for (key, value) in param_dict.items()}
    out_dict = {}
    if gen_data.breakpoint_lim:
        out_dict['Estimated t_cont'] = gen_data.est_t_cont
    if gen_data.fit_eq is not None:
        out_dict['Coefficient(s)'] = gen_data.params
        if gen_data.lof:
            out_dict['Limit of Fitting'] = gen_data.lof
        if gen_data.lod:
            out_dict['Limit of Detection'] = gen_data.lod
        if gen_data.mac:
            out_dict['Molar Absorption Coefficent'] = gen_data.mac
        if gen_data.mol0_fit is not None:
            out_dict['mol0_fit'] = gen_data.mol0_fit
        out_dict.update({'RSS': gen_data.rss,
                         'RMSE': gen_data.rmse,
                         'MAE': gen_data.mae,
                         'R2': gen_data.r2,
                         'R2_adj': gen_data.r2_adj,
                         'AIC': gen_data.aic,
                         'BIC': gen_data.bic})

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        if apply_data is not None:
            apply_data.all_df.to_excel(writer, sheet_name='ApplicationData', index=False)
        gen_data.all_df.to_excel(writer, sheet_name='GenerationData', index=False)
        if out_dict:
            pd.DataFrame.from_dict(out_dict).to_excel(writer, sheet_name='OutputParams', index=False)
        pd.DataFrame.from_dict(param_dict).to_excel(writer, sheet_name='InputParams', index=False)


def write_cc_fit_data_temp(param_dict, gen_data, apply_data):
    tmp_file = io.BytesIO()
    write_cc_fit_data(tmp_file, param_dict, gen_data, apply_data)

    return tmp_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


# print CC results
def pprint_cc(data):
    results = f""
    if data.num_spec == 1 and data.params is not None:
        results += f"""Parameters: { {item: f"{value:.4g}" for item, value in data.params[0].items()} }
Error: { {item: f"{value:.2g}" for item, value in data.param_err[0].items()} }\n
"""
        if data.breakpoint_lim:
            results += f"Estimated t_cont: {[f'{item:.4g}' for item in data.est_t_cont[0]]}\n"
        if data.lof is not None:
            results += f"Limits of Fitting: {data.lof[0]:.4g}\n"
        if data.mac is not None:
            results += f"Molar Absorption Coefficient: {data.mac[0]:.4g}\n"
        if data.mol0_fit is not None:
            results += f"Fitted initial moles: {data.mol0_fit[0]:.4g}\n"
        results += f"""
Quality of Fit Metrics:
RMSE: {data.rmse[0]:.4g} | MAE: {data.mae[0]:.4g}"""
        if data.r2:
            results += f"""
R²: {data.r2[0]:.4g} | Adjusted R²: {data.r2_adj[0]:.4g}
AIC: {data.aic[0]:.4g} | BIC: {data.bic[0]:.4g}\n
"""

    results += f"Download file to see full results"

    return results