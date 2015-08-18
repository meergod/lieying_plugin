using System;

// 本文件主要定义基于 .Net 实现猎影插件，对于一个插件类，需要
//  1、实现接口 IPlugin
//  2、指定 PluginAttribute 特性

namespace PluginFace {
    [Flags]
    public enum Function {
        /// <summary>
        /// 支持解析，Parse 和 ParseUrl 可用
        /// </summary>
        Parse = 0x001, 
        /// <summary>
        /// 支持搜索， Search 方法可用
        /// </summary>
        Search = 0x002,
        /// <summary>
        /// 支持配置, Config 和 ApplyConfig 方法可用
        /// </summary>
        Config = 0x100,
        /// <summary>
        /// 支持升级，Update 方法可用
        /// </summary>
        Update = 0x200
    }

    /// <summary>
    /// 用于说明本类为一个插件实现类
    /// 现在只支持一个模块中有一个插件实现类
    /// </summary>
    [AttributeUsage(AttributeTargets.Class)]
    public class PluginAttribute : Attribute {
        /// <summary>
        /// 指定本插件可用的功能
        /// </summary>
        public Function Functions { get; set; }
        /// <summary>
        /// 参见 Python 插件中的 GetVersion 
        /// </summary>
        public string Version { get; set; }
    }

    /// <summary>
    /// 该接口由猎影实现，用于插件显示一些信息
    /// </summary>
    public interface INotify {
        void Information( string str);
        void Warning(string str);
        void Error(string str);
    }

    /// <summary>
    /// Python 插件接口定义见 https://github.com/sceext2/lieying_plugin/blob/port_version-0.3/doc/lieying_plugin.md
    /// </summary>
    public interface IPlugin {
        /// <summary>
        /// 设置信息输出接口
        /// </summary>
        /// <param name="notify"></param>
        void SetNotifySink(INotify notify);
        /// <summary>
        /// 进行配置，参见 Python 插件中的 Config 中 参数 true 的情况
        /// </summary>
        void Config();
        /// <summary>
        /// 进行配置，参见 Python 插件中的 Config 中 参数 false 的情况
        /// </summary>
        void ApplyConfig();

        /// <summary>
        /// 对插件进行升级，参见 Python 插件中的 Update 
        /// </summary>
        /// <param name="path">为 null 则进行在线升级，非空为本地升级包的路径</param>
        string Update(string path);
        /// <summary>
        /// 与 ParseUrl 方法配对使用，本函数完成初步解析，参见 Python 插件中的 Parse
        /// </summary>
        /// <param name="url">要解析的网址</param>
        /// <returns></returns>
        string Parse(string url);
        /// <summary>
        /// 参见 Python 插件中的 ParseURL
        /// </summary>
        /// <param name="url">要解析的网址</param>
        /// <param name="label"></param>
        /// <param name="min"></param>
        /// <param name="max"></param>
        /// <returns></returns>
        string ParseUrl(string url, string label, int min, int max);
        /// <summary>
        /// 参见 Python 插件中的 Search 
        /// </summary>
        /// <param name="text"></param>
        /// <param name="start"></param>
        /// <param name="pageSize"></param>
        /// <param name="sortBy"></param>
        /// <param name="isDesc"></param>
        /// <returns></returns>
        string Search(string text, int start, int pageSize, string sortBy, bool isDesc);
    }
}
